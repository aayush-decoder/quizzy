from django.shortcuts import render
from django.http import HttpResponse
from django.urls import include, path
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.conf import settings

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Here you would typically authenticate the user
        # For example:
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password"
    return render(request, 'login.html')

def signup_view(request):
    return render(request, 'signup.html')

def forgetpass(request):
    return render(request, 'forgetpass.html')

def home_view(request):
    return render(request, '../templates/home.html')