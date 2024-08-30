from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def index(request):
    if request.method == 'POST':
        if 'register' in request.POST:  # Si c'est une inscription
            username = request.POST['username']
            password = request.POST['password']
            if User.objects.filter(username=username).exists():
                messages.error(request, "L'utilisateur existe déjà")
            else:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('index')
        elif 'login' in request.POST:  # Si c'est une connexion
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect")
    return render(request, 'index.html')

def user_logout(request):
    logout(request)
    return redirect('index')
