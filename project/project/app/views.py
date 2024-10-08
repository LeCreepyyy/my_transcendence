import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login
from .forms import LoginForm, RegisterForm, CheckBox2FAForm

from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode
import base64
from io import BytesIO
from django.http import HttpResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

    # verif register car pas finis et pas sur que sa marche theoriquement

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'User already exists')
            return render(request, 'register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already used')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()

        # totp_device = TOTPDevice.objects.create(user=user, name="Default TOTP Device")

        login(request, user)

        return redirect('user_login')
        # qr_code = reverse('setup_2fa')

    else:
        form = RegisterForm()

    # return render(request, 'register.html', {'qr_code': qr_code})
    return render(request, 'register.html', {'form': form})


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
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # request.session['pre_otp_user_id'] = user.id
            # return redirect('verify-otp')
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is wront')
    return render(request, 'login.html', {'form':form})

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
    
    return render(request, 'verify_otp.html')

@permission_classes([IsAuthenticated])
def home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    form = CheckBox2FAForm()

    if request.method == 'POST':
        form = CheckBox2FAForm(request.POST)
        if form.is_valid():
            checkbox_value = form.cleaned_data['checkbox']

            if checkbox_value:
                totp_device = TOTPDevice.objects.create(user=request.user, name="Default TOTP Device")
                device = TOTPDevice.objects.filter(user=request.user).first()
            
                totp_url = device.config_url
            
                qr = qrcode.make(totp_url)
                img = BytesIO()
                qr.save(img, "PNG")
                img.seek(0)

                qr_code_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    username = request.user.username
    return render(request, 'home.html', {'form': form, 'username': username})


def default(request):
    return redirect('user_login')