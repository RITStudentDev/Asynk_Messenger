from rest_framework import serializers
from .models import User
import string
from django.utils.crypto import get_random_string

# General serializer for user data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'contact']

# Serializes information in database to be used during user creation
class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

        # Check if entered email is already in use
        def validate_email(self, value):
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError('Account already exists with this email')
            return value
        
        # Check if both entered passwords are the same
        def validate_password(self, value):
            if value['password'] != value['password2']:
                raise serializers.ValidationError({'password2': 'Passwords do not match'})
            return value

        # Generates 9 digit contact
        def generate_contact(self):
            if User.objects.count < 900000000:
                while True:
                    contact = get_random_string(9, allowed_chars=string.digits)
                    if not User.objects.filter(unique_id=contact).exists():
                        return contact
            raise Exception('Max user count reached')

        # Add new user to database
        def create(self, validated_data):
            validated_data.pop('password2')
            password = validated_data.pop('password')
            user = User(**validated_data)
            # create function to add the password

            if not self.contact:
                self.contact = self.generate_contact()

            user.save()
            return user
