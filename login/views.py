from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User

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
            return render(request, 'home.html', {'error_message': error_message})
    return render(request, 'login2.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        conpass = request.POST.get('confirm_password')
        email = request.POST.get('email')
        # Here you would typically create a new user
        # For example:
        # user = User.objects.create_user(username=username, password=password, email=email)
        # user.save()
        # return redirect('login')
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)  # Set the password using set_password method
        if password == conpass:
            user.save()
            return redirect('login')
        else:
            error_message = "Passwords do not match"
            return render(request, 'signup.html', {'error_message': error_message})
        
       
    return render(request, 'signup.html')

def forgetpass(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        # email = request.POST.get('email')
        # Here you would typically handle the password reset logic
        # For example, send a password reset email or redirect to a password reset page
        user = User.objects.filter(username=username).first()
        if user:
            # Logic to send password reset email or redirect to password reset page
            return redirect('login')
        else:
            error_message = "User not found"
            return render(request, 'forgetpass.html', {'error_message': error_message})
    return render(request, 'forgetpass.html')

def home_view(request):
    return render(request,'home.html')