from django.shortcuts import render, request
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

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

        return redirect('login')


    return render(request, 'profil.html')

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
