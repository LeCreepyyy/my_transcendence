import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

from django_otp.plugins.otp_totp.models import TOTDevice
import qrcode
from io import BytesIO
from django.http import HttpResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'User already exists')
            return render(request, 'profil.html')
        
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()

        totp_device = TOTPDevice.objects.create(user=user, name="Default TOTP Device")

        login(request, user)

        return redirect('setup_2fa')

    return render(request, 'profil.html')

def setup_2fa(request):
    user = request.user
    device = TOTPDevice.objects.get(user=user)

    totp_url = device.config_url

    qr = qrcode.make(totp_url)
    img = BytesIO()
    qr.save(img, "PNG")
    img.seek(0)

    return HttpResponse(img.getvalue(), content_type="image/png")

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session['pre_otp_user_id'] = user.id
            return redirect('verify-otp')
        else:
            messages.error(request, 'Username or Password is wront')
    return render(request, 'profil.html')

def verify_otp(request):
    if request.method == 'POST':
        otp_token = request.POST.get('otp_token')

        # Récupérer l'utilisateur pré-authentifié
        user_id = request.session.get('pre_otp_user_id')
        user = User.objects.get(id=user_id)

        # Chercher un appareil TOTP lié à l'utilisateur
        totp_device = TOTPDevice.objects.filter(user=user).first()

        if totp_device and totp_device.verify_token(otp_token):
            # Authentifier l'utilisateur complètement
            login(request, user)
            # Supprimer l'information de session temporaire
            del request.session['pre_otp_user_id']
            

            # Génération des tokens JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Création de la réponse et ajout d'un cookie pour le token JWT
            response = redirect('home')  # Rediriger vers la page d'accueil
            response.set_cookie('access_token', access_token, httponly=True, samesite='Lax')

            # Vous pouvez également définir un cookie pour le refresh token si nécessaire
            response.set_cookie('refresh_token', str(refresh), httponly=True, samesite='Lax')

            return response

        else:
            messages.error(request, 'OTP invalid.')
    
    return render(request, 'profil.html')

@permission_classes([IsAuthenticated])
def home(request):
    return render(request, 'profil.html')
