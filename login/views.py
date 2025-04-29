from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from myquiz.models import QuizResult, Quiz

from django.db.models import Avg

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
            print("Authentication failed")
            return render(request, 'login2.html', {'error_message': error_message})
    return render(request, 'login2.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        conpass = request.POST.get('confirm_password')
        email = request.POST.get('email')

        # Check if passwords match
        if password != conpass:
            error_message = "Password and Confirm Password do not match"
            return render(request, 'signup.html', {'error_message': error_message})

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            error_message = "Username already exists"
            return render(request, 'signup.html', {'error_message': error_message})
        if User.objects.filter(email=email).exists():
            error_message = "Email already exists"
            return render(request, 'signup.html', {'error_message': error_message})

        # Create the user after all checks
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)  # Set the password using set_password method
        user.save()
        return render(request,'login')
    return render(request, 'signup.html')

from django.core.mail import send_mail
from django.conf import settings

def forgetpass(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            # Generate a new password or use the existing one
            #fetch the user password
            password = user.password

            # Send the password to the user's email
            subject = "Password Reset Request"
            message = f"Hello {user.username},\n\nYour  password is: {password}\n\nPlease log in and change your password immediately."
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list)

            return redirect('login')
        else:
            error_message = "User not found"
            return render(request, 'forgetpass.html', {'error_message': error_message})
    return render(request, 'forgetpass.html')






def home_view(request):
    # avg_rating = QuizResult.objects.aggregate(avg_rating=Avg('rating_by_user'))['avg_rating'] or 0

    # context = {
    #     'avg_rating': round(avg_rating, 1), 
    # }
    # print(avg_rating)

    return render(request, 'home.html')
