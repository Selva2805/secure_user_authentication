from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirect to a different page after login, e.g., 'home'
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'signup.html')  # Re-render the login page with an error message
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email,
                    first_name=first_name, last_name=last_name
                )
                user.save()
                messages.success(request, 'User created successfully')
                return redirect('login')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
    else:
        return render(request, 'signup.html')
def home(request):
    return render(request, 'home.html')
def logout(request):
    auth_logout(request)
    return redirect('login')