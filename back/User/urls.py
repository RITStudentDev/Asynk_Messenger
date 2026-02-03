from django.urls import path, include
from .views import CustomTokenObtainPairView, CustomTokenRefreshView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)