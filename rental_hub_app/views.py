from django.shortcuts import render,redirect
from .models import *
from . import models
import datetime
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Create your views here.
def login_meth(request):
    if request.method=="POST":
        errors=User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            # save previous data input in session to display them in directed page
            request.session['log_email']=request.POST['log_email']
            request.session['log_password']=request.POST['log_password']
            return redirect('/')
        else:
            if models.validate_login(request.POST):
                users_list=User.objects.filter(email=request.POST['log_email'])
                user=users_list[0]
                if user:
                    logged_user=users_list[0]
                    request.session['logged']=True
                    request.session['logged_in_user_id']=logged_user.id
                    request.session['logged_in_user_name']=logged_user.first_name +' '+logged_user.last_name
                    # delete data from session
                    if 'log_email' in request.session:
                        del request.session['log_email']
                    if 'log_password' in request.session:
                        del request.session['log_password']
                    request.session.modified = True
                if user.role == Role.objects.get(title='host'):
                    return redirect('/received')
                elif user.role == Role.objects.get(title='guest'):
                    return redirect('/sent')
                elif user.role == Role.objects.get(title='admin'):
                    return redirect('/admin_board')
                else:
                    return render(request,'insufficient_priv.html')
                    
            else:
                return redirect('/')
    else:
        return render(request,'login.html')

def register_meth(request):
    if request.method=="POST":
        errors=User.objects.create_new_user_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            # save previous data input in session to display them again
            request.session['first_name']=request.POST['first_name']
            request.session['last_name']=request.POST['last_name']
            request.session['email']=request.POST['email']
            request.session['password']=request.POST['password']
            request.session['password_confirm']=request.POST['password_confirm']
            request.session['phone_1']=request.POST['phone_1']
            request.session['phone_2']=request.POST['phone_2']
            request.session['role']=request.POST['role']
            request.session['address']=request.POST['address']
            return redirect('/register')
        else:
            add_user(request.POST)
            # delete data from session
            if 'first_name' in request.session:
                del request.session['first_name']
            if 'last_name' in request.session:
                del request.session['last_name']
            if 'email' in request.session:
                del request.session['email']
            if 'password' in request.session:
                del request.session['password']
            if 'password_confirm' in request.session:
                del request.session['password_confirm']
            if 'phone_1' in request.session:
                del request.session['phone_1']
            if 'phone_2' in request.session:
                del request.session['phone_2']
            if 'role' in request.session:
                del request.session['role']
            if 'address' in request.session:
                del request.session['address']
            request.session.modified = True
            return redirect('/')
    else:
        roles = Role.objects.exclude(title='admin')
        context = {
        'roles': roles}
        return render(request,'register.html',context)
    
def insufficient_priv_meth(request):
    return render(request,'insufficient_priv.html')

def logout_meth(request):
    # delete data from session
    if 'logged' in request.session:
        del request.session['logged']
        print("logged")
    if 'logged_in_user_name' in request.session:
        del request.session['logged_in_user_name']
        print("logged_in_user_name")
    if 'logged_in_user_id' in request.session:
        del request.session['logged_in_user_id']
        print("logged_in_user_id")
    request.session.modified = True
    return redirect('/')

def add_property_meth(request):
    # if request.method=="POST":
    if request.method == "POST":
        image = request.FILES.get("image") 
        errors=Property.objects.create_new_property_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            # save previous data input in session to display them again
            # 20 item
            request.session['type']=request.POST['type']
            request.session['rent_type']=request.POST['rent_type']
            request.session['area']=request.POST['area']
            request.session['elevator']=request.POST['elevator']
            request.session['rent_allowance']=request.POST['rent_allowance']
            request.session['num_bedrooms']=request.POST['num_bedrooms']
            request.session['num_living_rooms']=request.POST['num_living_rooms']
            request.session['num_kitchens']=request.POST['num_kitchens']
            request.session['num_balconies']=request.POST['num_balconies']
            request.session['num_bathrooms']=request.POST['num_bathrooms']
            request.session['num_air_conditions']=request.POST['num_air_conditions']
            request.session['num_parkings']=request.POST['num_parkings']
            request.session['internet_service']=request.POST['internet_service']
            request.session['city']=request.POST['city']
            request.session['address']=request.POST['address']
            request.session['is_vacant']=request.POST['is_vacant']
            request.session['rent_start_date']=request.POST['rent_start_date']
            request.session['rent_end_date']=request.POST['rent_end_date']
            request.session['notes_host']=request.POST['notes_host']
            request.session['notes_host_private']=request.POST['notes_host_private']
            # request.session['image_1']=request.FILES["image_1"]
            # request.session['image_2']=request.FILES["image_2"]
            # request.session['image_1_title']=request.POST["image_1_title"]
            # request.session['image_2_title']=request.POST["image_2_title"]
            # request.session['image']=request.FILES["image"]
            return redirect('/add-property')
        else:
            add_property(request.POST,request.FILES)
            # delete data from session
            if 'type' in request.session:
                del request.session['type']
            if 'rent_type' in request.session:
                del request.session['rent_type']
            if 'area' in request.session:
                del request.session['area']
            if 'elevator' in request.session:
                del request.session['elevator']
            if 'rent_allowance' in request.session:
                del request.session['rent_allowance']
            if 'num_bedrooms' in request.session:
                del request.session['num_bedrooms']
            if 'num_living_rooms' in request.session:
                del request.session['num_living_rooms']
            if 'num_kitchens' in request.session:
                del request.session['num_kitchens']
            if 'num_balconies' in request.session:
                del request.session['num_balconies']
            if 'num_bathrooms' in request.session:
                del request.session['num_bathrooms']
            if 'num_air_conditions' in request.session:
                del request.session['num_air_conditions']
            if 'num_parkings' in request.session:
                del request.session['num_parkings']
            if 'internet_service' in request.session:
                del request.session['internet_service']
            if 'city' in request.session:
                del request.session['city']
            if 'address' in request.session:
                del request.session['address']
            if 'is_vacant' in request.session:
                del request.session['is_vacant']
            if 'rent_start_date' in request.session:
                del request.session['rent_start_date']
            if 'rent_end_date' in request.session:
                del request.session['rent_end_date']
            if 'notes_host' in request.session:
                del request.session['notes_host']
            if 'notes_host_private' in request.session:
                del request.session['notes_host_private']
            # if 'image' in request.session:
            #     del request.session['image']
            # if 'image_1' in request.session:
            #     del request.session['image_1']
            # if 'image_2' in request.session:
            #     del request.session['image_2']
            # if 'image_1_title' in request.session:
            #     del request.session['image_1_title']
            # if 'image_2_title' in request.session:
            #     del request.session['image_2_title']
            request.session.modified = True
            return redirect('/my_properties')
    else:
        property_types = Type.objects.all()
        rent_types = Rent_type.objects.all()
        cities = City.objects.all()
        context = {
        'property_types': property_types,
        'rent_types':rent_types,
        'cities':cities}
        
        return render(request,'property_add.html',context)
def edit_property_meth(request,id):
    if request.method=="POST":
        errors=Property.objects.create_new_property_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            # 20 item
            request.session['type']=request.POST['type']
            request.session['rent_type']=request.POST['rent_type']
            request.session['area']=request.POST['area']
            request.session['elevator']=request.POST['elevator']
            request.session['rent_allowance']=request.POST['rent_allowance']
            request.session['num_bedrooms']=request.POST['num_bedrooms']
            request.session['num_living_rooms']=request.POST['num_living_rooms']
            request.session['num_kitchens']=request.POST['num_kitchens']
            request.session['num_balconies']=request.POST['num_balconies']
            request.session['num_bathrooms']=request.POST['num_bathrooms']
            request.session['num_air_conditions']=request.POST['num_air_conditions']
            request.session['num_parkings']=request.POST['num_parkings']
            request.session['internet_service']=request.POST['internet_service']
            request.session['city']=request.POST['city']
            request.session['address']=request.POST['address']
            request.session['is_vacant']=request.POST['is_vacant']
            request.session['rent_start_date']=request.POST['rent_start_date']
            request.session['rent_end_date']=request.POST['rent_end_date']
            request.session['notes_host']=request.POST['notes_host']
            request.session['notes_host_private']=request.POST['notes_host_private']
    
            return redirect(f'/edit-property/{request.POST['id']}')
        else:
            update_property(request.POST,request.FILES,request.session['logged_in_user_id'])
            # delete data from session
            if 'type' in request.session:
                del request.session['type']
            if 'rent_type' in request.session:
                del request.session['rent_type']
            if 'area' in request.session:
                del request.session['area']
            if 'elevator' in request.session:
                del request.session['elevator']
            if 'rent_allowance' in request.session:
                del request.session['rent_allowance']
            if 'num_bedrooms' in request.session:
                del request.session['num_bedrooms']
            if 'num_living_rooms' in request.session:
                del request.session['num_living_rooms']
            if 'num_kitchens' in request.session:
                del request.session['num_kitchens']
            if 'num_balconies' in request.session:
                del request.session['num_balconies']
            if 'num_bathrooms' in request.session:
                del request.session['num_bathrooms']
            if 'num_air_conditions' in request.session:
                del request.session['num_air_conditions']
            if 'num_parkings' in request.session:
                del request.session['num_parkings']
            if 'internet_service' in request.session:
                del request.session['internet_service']
            if 'city' in request.session:
                del request.session['city']
            if 'address' in request.session:
                del request.session['address']
            if 'is_vacant' in request.session:
                del request.session['is_vacant']
            if 'rent_start_date' in request.session:
                del request.session['rent_start_date']
            if 'rent_end_date' in request.session:
                del request.session['rent_end_date']
            if 'notes_host' in request.session:
                del request.session['notes_host']
            if 'notes_host_private' in request.session:
                del request.session['notes_host_private']
            request.session.modified = True
            return redirect(f'/view-property/{id}')
    else:
        property_types = Type.objects.all()
        rent_types = Rent_type.objects.all()
        cities = City.objects.all()
        
        property_list=Property.objects.filter(id=id)
        if property_list[0]:
            property=property_list[0]
            images_list=Image.objects.filter(property=property)
        else:
            property="Record does not exists"
        context = {
                    'property_types': property_types,
                    'rent_types':rent_types,
                    'cities':cities,
                    'property':property,
                    'images_list':images_list}
        return render(request,'property_edit.html',context)
    
def view_property_meth(request,id):
    property_list=Property.objects.filter(id=id)
    if property_list[0]:
        property=property_list[0]
        images_list=Image.objects.filter(property=property)
    else:
        property="Record does not exists"
    context = {'property':property,
                'images_list':images_list}
    
    return render(request,'property_view.html',context)

def delete_property_meth(request,id):
    if request.session.get('logged'):
        # only creator can delete this object
        property_list=Property.objects.filter(id=id)
        property_db=property_list[0]
        if request.session.get('logged_in_user_id') == property_db.owner.id:
            delete_property(id)
            return redirect('/my_properties')
        else:
            return redirect(f"/insufficient_privileges")
    else:
        return redirect('/')
def my_properties_meth(request):
    if request.session.get('logged'):
        # for owner , we display all properties of logged in owner
        logged_in_user_list=User.objects.filter(id=request.session['logged_in_user_id'])
        logged_in_user=logged_in_user_list[0]
        property_list=Property.objects.filter(owner=logged_in_user)
        p = Paginator(property_list, 12) 
        page_number = request.GET.get('page') 
        try:
            page_obj = p.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = p.page(p.num_pages)
        context = {'page_obj': page_obj}
        return render(request,'property_my_properties.html',context)
    else:
        return redirect('/')