from django.shortcuts import render

def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'signup.html')

def quiz(request):
    return render(request, 'quiz.html')