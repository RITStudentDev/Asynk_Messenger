from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import SignupSerializer, UserSerializer
from .models import AsynkUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomTokenObtainPairView(TokenObtainPairView):
    def post (self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            access_token = tokens.get('access')
            refresh_token = tokens.get('refresh')

            res = Response()
            res.data = {'tokenGenerated': True}

            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax', 
                path='/',
            )

            res.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                path='/',
            )
            return res
        except Exception as e:
            return Response({'tokenGenerated': False, 'error': str(e)}, status=400)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            access_token = tokens['access']

            res = Response()
            res.data = {'tokenRefreshed': True}

            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/',
            )
            return res
        except Exception as e:
            return Response({'tokenRefreshed': False, 'error': str(e)}, status=400)
        
class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get('access_token')
        if raw_token is None:
            return super().authenticate(request)
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token

class UserViewSet(ModelViewSet):
    queryset = AsynkUser.objects.all()
    authentication_classes = [CookieJWTAuthentication]

    # Use signup serializer only on user creation and user serializer everywhere else
    def get_serializer_class(self):
        if self.action == 'create':
            return SignupSerializer
        return UserSerializer
    
    # Use authentication everywhere except user creation
    def get_permissions(self):
        if self.action in ['create', 'login']:
            return [AllowAny()]
        return [IsAuthenticated()]
    
    # Sets queryset to fetch data for only the authenticated user
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return AsynkUser.objects.filter(id=self.request.user.id)
        return AsynkUser.objects.none()
    
    # implement function to get all data on a user
    def retrieve(self, request, pk=None):
        user = request.user
        serializer = self.get_serializer(user)

        return Response(serializer.data)
    

    