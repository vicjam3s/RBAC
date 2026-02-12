from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import CustomUserCreationForm, CustomAuthForm
from .models import User, UserRole, Role


def index(request):
    """Homepage"""
    if request.user.is_authenticated:
        return redirect('admin:index')
    return render(request, 'index.html')


@require_http_methods(["GET", "POST"])
def registration_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Assign default role (Reader) to new users
            reader_role = Role.objects.filter(name=Role.READER).first()
            if reader_role:
                UserRole.objects.create(user=user, role=reader_role)
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('rbac_app:login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('admin:index')
    
    if request.method == 'POST':
        form = CustomAuthForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome {user.email}!')
            return redirect('admin:index')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = CustomAuthForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('rbac_app:index')