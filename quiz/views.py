from django.shortcuts import render, redirect

from django.contrib.auth import logout

def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'signup.html')

def feedback_form_view(request):
    return render(request, "feedback.html")

def admin(request):
    return render(request,"home.html")


def logout_view(request):
    logout(request)
    return redirect('home')

def about_view(request):
    return render(request, "aboutus.html")