from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from two_factor.urls import urlpatterns as tf_urls
from django.contrib.auth import views as auth_views

from app.views import register, home, TwoFactorLoginWithJWT

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include(tf_urls)),

    path('account/login/', TwoFactorLoginWithJWT.as_view(), name='login'),
    # path('account/login/', auth_views.LoginView.as_view(), name='login'),

    path('register/', register, name='register'),

    path('home/', home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)