import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
            return render(request, 'register.html', {'form': form})
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already used')
            return render(request, 'register.html', {'form': form})

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()

        login(request, user)

        return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def home(request):
    username = request.user
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'home.html')