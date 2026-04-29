from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User

# Extended the default UserCreationForm to include an email field
# Django doesn't include email by default so I had to add it manually
class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

from django.contrib import messages


# Renders the landing/home page - no login required
def home(request):
    return render(request, 'home.html')


# Handles login - redirects to home if already logged in
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Show a welcome message after successful login
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


# Handles new user registration
def register_view(request):
    if request.user.is_authenticated:
        redirect('dashboard')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in straight after registering so they don't have to sign in again
            login(request, user)
            messages.success(request, f'Account created! Welcome, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# Logs the user out and sends them back to the login page
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


from django.contrib.auth.decorators import login_required

# login_required means if you're not logged in, Django redirects you to the login page
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# Forgot password just tells users to contact admin - no self-service reset for now
def forgot_password(request):
    return render(request, 'accounts/forgot_password.html')
