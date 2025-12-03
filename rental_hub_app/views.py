from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db import IntegrityError
import re


def about_us(request):
    """About Us page"""
    return render(request, 'rent_app/about_us.html')


def login_view(request):
    """Login page view"""
    error_message = None
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        if not email or not password:
            error_message = "Please fill in all fields."
        else:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                error_message = "Invalid email or password. Please try again."
    
    return render(request, 'rent_app/login.html', {'error_message': error_message})


def register_view(request):
    """Register page view"""
    errors = {}
    roles = Role.objects.all()
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        phone_1 = request.POST.get('phone_1', '').strip()
        phone_2 = request.POST.get('phone_2', '').strip()
        address = request.POST.get('address', '').strip()
        role_id = request.POST.get('role', '')
        
        # Server-side validation
        if not first_name:
            errors['first_name'] = "First name is required."
        if not last_name:
            errors['last_name'] = "Last name is required."
        if not email:
            errors['email'] = "Email is required."
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors['email'] = "Please enter a valid email address."
        else:
            # Check if email already exists
            if User.objects.filter(email=email).exists():
                errors['email'] = "This email is already registered."
        
        if not password:
            errors['password'] = "Password is required."
        elif len(password) < 8:
            errors['password'] = "Password must be at least 8 characters long."
        
        if not confirm_password:
            errors['confirm_password'] = "Please confirm your password."
        elif password != confirm_password:
            errors['confirm_password'] = "Passwords do not match."
        
        if not phone_1:
            errors['phone_1'] = "Phone 1 is required."
        else:
            # Remove all non-digit characters for validation
            phone_digits = re.sub(r'\D', '', phone_1)
            if len(phone_digits) < 10:
                errors['phone_1'] = "Phone number must be at least 10 digits."
        
        # Validate phone_2 if provided
        if phone_2:
            phone2_digits = re.sub(r'\D', '', phone_2)
            if len(phone2_digits) < 10:
                errors['phone_2'] = "Phone number must be at least 10 digits."
        
        if not address:
            errors['address'] = "Address is required."
        
        if not role_id:
            errors['role'] = "Please select a role."
        
        # If no errors, create user
        if not errors:
            try:
                role = Role.objects.get(id=role_id)
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    phone_1=phone_1,
                    phone_2=phone_2 if phone_2 else None,
                    address=address,
                    role=role
                )
                messages.success(request, 'Registration successful! Please login.')
                return redirect('login')
            except Role.DoesNotExist:
                errors['role'] = "Invalid role selected."
            except IntegrityError:
                errors['email'] = "This email is already registered."
            except Exception as e:
                errors['general'] = f"An error occurred: {str(e)}"
        
        # Return form data and errors for re-display
        context = {
            'errors': errors,
            'roles': roles,
            'form_data': {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone_1': phone_1,
                'phone_2': phone_2,
                'address': address,
                'role': role_id,
            }
        }
        return render(request, 'rent_app/register.html', context)
    
    return render(request, 'rent_app/register.html', {'errors': {}, 'form_data': {}, 'roles': roles})


def profile_view(request):
    """Profile page view - shows user info after login"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    context = {
        'user': user,
        'role_title': user.get_role_title(),
    }
    return render(request, 'rent_app/profile.html', context)

def user_dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    
    user = User.objects.get(id=request.session['user_id'])
    properties = Property.objects.filter(owner=user)
    
    context = {
        "user": user,
        "properties": properties
    }
    return render(request, "user_dashboard.html", context)
