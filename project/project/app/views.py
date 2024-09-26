import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

from django_otp.plugins.otp_totp.models import TOTDevice
import qrcode
from io import BytesIO
from django.http import HttpResponse

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

        return redirect('user_login') # changer par 'setup_2fa'

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
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password is wront')
    return render(request, 'profil.html')

def home(request):
    return render(request, 'profil.html')
