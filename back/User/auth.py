from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        access_token = request.COOKIES.get('access_token')
        if access_token is None:
            return None
        
        validated_token = self.getValidated_token(access_token)
        try:
            user = self.get_user(validated_token)
        except:
            return None