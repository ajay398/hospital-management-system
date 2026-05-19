from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .email_service import send_email

from .models import User



def signup_view(request):

    error = None

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        if User.objects.filter(email=email).exists():

            error = "Email already exists"

            return render(
                request,
                'accounts/signup.html',
                {'error': error}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        login(request, user)

        send_email(
            user.email,
            "Welcome to HMS",
            f"Hello {user.username}, welcome to HMS."
        )

        return redirect('dashboard')

    return render(request, 'accounts/signup.html')


def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

    return render(request, 'accounts/login.html')

@login_required
def dashboard_view(request):

    if request.user.role == 'doctor':
        return render(request, 'accounts/doctor_dashboard.html')

    elif request.user.role == 'patient':
        return render(request, 'accounts/patient_dashboard.html')

    return redirect('login')


def logout_view(request):

    logout(request)

    return redirect('login')