from . import views
from django.urls import path 
from django.shortcuts import redirect

def redirect_to_login(request):
    return redirect('login')
urlpatterns = [
    path('', redirect_to_login, name='home'),
    path('about-us/', views.about_us, name='about_us'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
	]