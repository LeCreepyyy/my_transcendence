from django.contrib import admin
from django.urls import path, include

#from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app.views import user_login, register, home, verify_otp

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api-auth/', include('rest_framework.urls')), # "api-auth/login/"
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include('two_factor.urls', 'two_factor')),

    path('login/', user_login, name='user_login'),
    path('verify_otp', verify_otp, name='verify_otp'),

    path('register/', register, name='register'),
    path('home/', home, name='home'),
]
