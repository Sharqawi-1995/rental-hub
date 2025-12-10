from django.db import models
import bcrypt
import re
import datetime 
from django.core.files.storage import default_storage
import os

class User_Manager(models.Manager):
    def create_new_user_validator(self,postData):
        errors={}
        first_name=postData.get('first_name')
        last_name=postData.get('last_name')
        email=postData.get('email')
        password=postData.get('password')
        password_confirm=postData.get('password_confirm')
        phone_1=postData.get('phone_1')
        phone_2=postData.get('phone_2')
        role=postData.get('role')
        address=postData.get('address')
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if len(first_name) <=2 :
            errors["first_name"]="First name should be at least 2 chars"
        if len(last_name) <= 2 :
            errors["last_name"]="Last name should be at least 2 chars"
        if len(phone_1) != 10 :
            errors["phone_1"]="First phone number should be 10 digits"
        if phone_2:
            if len(phone_2) != 10 :
                errors["phone_2"]="Second phone number should be 10 digits"
        if len(address) <= 2 :
            errors["address"]="Address should be at least 3 chars"
        if len(role) == 0 :
            errors["role"]="Role should be selected"
        if len(email) == 0:
            errors["email"]="E-mail should be filled "
        else:
            if not EMAIL_REGEX.match(email):
                errors['email'] = "Invalid e-mail address!"
            else:
                if User.objects.filter(email=email).exists() :
                    errors["email"]="E-mail Exists , Try a new one" 
        if len(password) < 8:
            errors["password"]="Password should be at least 8 chars"
        if len(password_confirm) < 8:
            errors["password_confirm"]="Password Confirmation should be at least 8 chars"
        if len(password) >=8 and len(password_confirm) >= 8:
            if not password==password_confirm:
                errors["password"]="Password Mismatch"
        return errors
    # for login page error validation
    def login_validator(self,postData):
        errors={}
        email=postData.get('log_email')
        password=postData.get('log_password')
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if len(email) == 0:
            errors["log_email"]="E-mail should be filled "
        else:
            if not EMAIL_REGEX.match(email):
                errors['log_email'] = "Invalid e-mail address!" 
        if len(password) < 8:
            errors["log_password"]="Password should be at least 8 chars"
        if EMAIL_REGEX.match(email) and len(password) >= 8:
            if not validate_login(postData):
                errors['log_email'] = "Invalid Credentials!"
        return errors
    
# User models with 10 attributes
class User(models.Model):
    first_name=models.CharField(max_length=15)
    last_name=models.CharField(max_length=15)
    email=models.CharField(max_length=20)
    password=models.CharField(max_length=255)
    phone_1=models.CharField(max_length=255)
    phone_2=models.CharField(max_length=15)
    role=models.ForeignKey('Role',related_name="users",on_delete=models.CASCADE)
    address=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=User_Manager()
    def __str__(self):
        return self.first_name+ ' '+ self.last_name
    
def add_user(form):
    pass_hash=bcrypt.hashpw(form['password'].encode(),bcrypt.gensalt()).decode()
    new_user=User.objects.create(
                                first_name=form['first_name'],
                                last_name=form['last_name'],
                                email=form['email'],
                                password=pass_hash,
                                phone_1=form['phone_1'],
                                phone_2=form['phone_2'],
                                role=Role.objects.get(id=form['role']),
                                address=form['address']
    )
    
# method to check login credential are matching  
def validate_login(form):
    user=User.objects.filter(email=form['log_email'])
    if user:
        logged_user=user[0]
        email=logged_user.email
        password=logged_user.password
        form_pass=form['log_password']
        if bcrypt.checkpw(form_pass.encode(),password.encode()):
            return True
        else:
            return False
# for login page error validation
    def login_validator(self,postData):
        errors={}
        email=postData.get('log_email')
        password=postData.get('log_password')
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if len(email) == 0:
            errors["log_email"]="E-mail should be filled "
        else:
            if not EMAIL_REGEX.match(email):
                errors['log_email'] = "Invalid e-mail address!" 
        if len(password) < 8:
            errors["log_password"]="Password should be at least 8 chars"
        if EMAIL_REGEX.match(email) and len(password) >= 8:
            if not validate_login(postData):
                errors['log_email'] = "Invalid Credentials!"
        return errors
    
class Property_Manager(models.Manager):
    def create_new_property_validator(self,postData):
        errors={}
        type=postData.get('type')
        rent_type=postData.get('rent_type')
        area=postData.get('area')
        elevator=postData.get('elevator')
        rent_allowance=postData.get('rent_allowance')
        num_bedrooms=postData.get('num_bedrooms')
        num_living_rooms=postData.get('num_living_rooms')
        num_kitchens=postData.get('num_kitchens')
        num_balconies=postData.get('num_balconies')
        num_bathrooms=postData.get('num_bathrooms')
        num_air_conditions=postData.get('num_air_conditions')
        num_parkings=postData.get('num_parkings')
        internet_service=postData.get('internet_service')
        city=postData.get('city')
        address=postData.get('address')
        is_active=postData.get('is_active')
        is_vacant=postData.get('is_vacant')
        rent_start_date=postData.get('rent_start_date')
        rent_end_date=postData.get('rent_end_date')
        
        if len(type) == 0 :
            errors["type"]="Type should be selected"
        if len(rent_type) == 0 :
            errors["rent_type"]="Rent Type should be selected"
        if len(area) == 0 :
            errors["area"]="Area should be filled"
        if len(elevator) == 0 :
            errors["elevator"]="Elevator should be selected"
        if len(rent_allowance) == 0 :
            errors["rent_allowance"]="Rent allowence should be filled"
        if len(num_bedrooms) == 0 :
            errors["num_bedrooms"]="Number of bedrooms should be defined"
        if len(num_living_rooms) == 0 :
            errors["num_living_rooms"]="Number of living rooms should be defined"
        if len(num_kitchens) == 0 :
            errors["num_kitchens"]="Number of Kitchens should be defined"
        if len(num_balconies) == 0 :
            errors["num_balconies"]="Number of Balconies should be defined"
        if len(num_bathrooms) == 0 :
            errors["num_bathrooms"]="Number of bathrooms should be defined"
        if len(num_air_conditions) == 0 :
            errors["num_air_conditions"]="Number of air conditions should be defined"
        if len(num_parkings) == 0 :
            errors["num_parkings"]="Number of parkings should be defined"
        if len(internet_service) == 0 :
            errors["internet_service"]="Internet serivce should be selected"
        if len(city) == 0 :
            errors["city"]="City should be selected"
        if len(address) == 0 :
            errors["address"]="Address should be filled"
        if len(is_vacant) == 0 :
            errors["is_vacant"]="Is-Vacant status should be selected"
        else:
            if is_vacant==False:
                if len(rent_start_date) == 0:
                    errors["rent_start_date"]="Rent start date should be selected"
                if len(rent_end_date) == 0:
                    errors["rent_end_date"]="Rent end date should be selected"
        return errors
            
class Property(models.Model):
    owner=models.ForeignKey(User,related_name="properties",on_delete=models.CASCADE)
    type=models.ForeignKey('Type',related_name="properties",on_delete=models.CASCADE,null=True)
    rent_type=models.ForeignKey('Rent_type',related_name="properties",on_delete=models.CASCADE,null=True)
    area=models.PositiveIntegerField(default=0)
    elevator=models.BooleanField(default=False)
    rent_allowance=models.PositiveIntegerField(default=0)
    num_bedrooms=models.PositiveIntegerField(default=0)
    num_living_rooms=models.PositiveIntegerField(default=0)
    num_kitchens=models.PositiveIntegerField(default=0)
    num_balconies=models.PositiveIntegerField(default=0)
    num_bathrooms=models.PositiveIntegerField(default=0)
    num_air_conditions=models.PositiveIntegerField(default=0)
    num_parkings=models.PositiveIntegerField(default=0)
    internet_service=models.BooleanField(default=False)
    city=models.ForeignKey('City',related_name="properties",on_delete=models.CASCADE,null=True)
    address=models.TextField(blank=True, null=True)
    is_active=models.BooleanField(default=False)
    is_vacant=models.BooleanField(default=False)
    rent_start_date=models.DateField()
    rent_end_date=models.DateField()
    notes_host=models.TextField(blank=True, null=True)
    notes_host_private=models.TextField(blank=True, null=True)
    notes_admin_to_host=models.TextField(blank=True, null=True)
    notes_admin_private=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=Property_Manager()

# only for hosts
def add_property(form,file):
    property=Property.objects.create(
    owner=User.objects.get(id=form['owner']),
    type=Type.objects.get(id=form['type']),
    rent_type=Rent_type.objects.get(id=form['rent_type']),
    area=form['area'],
    elevator=form['elevator'],
    rent_allowance=form['rent_allowance'],
    num_bedrooms=form['num_bedrooms'],
    num_living_rooms=form['num_living_rooms'],
    num_kitchens=form['num_kitchens'],
    num_balconies=form['num_balconies'],
    num_bathrooms=form['num_bathrooms'],
    num_air_conditions=form['num_air_conditions'],
    num_parkings=form['num_parkings'],
    internet_service=form['internet_service'],
    city=City.objects.get(id=form['city']),
    address=form['address'],
    # is_active=form['is_active'],
    is_vacant=form['is_vacant'],
    rent_start_date=form['rent_start_date'],
    rent_end_date=form['rent_end_date'],
    notes_host=form['notes_host'],
    notes_host_private=form['notes_host_private']
    )
    if 'image_1' in file:
        image_1= Image.objects.create(property=property,
                                        image=file['image_1'],
                                        title=form['image_1_title'])
        property.images.add(image_1)
        
    if 'image_2' in file:  
        image_2= Image.objects.create(property=property,
                                        image=file['image_2'],
                                        title=form['image_2_title'])
        property.images.add(image_2)
    if 'image_3' in file:    
        image_3= Image.objects.create(property=property,
                                        image=file['image_3'],
                                        title=form['image_3_title'])
        property.images.add(image_3)
    if 'image_4' in file: 
        image_4= Image.objects.create(property=property,
                                        image=file['image_4'],
                                        title=form['image_4_title'])
        property.images.add(image_4)
        
    if 'image_5' in file:    
        image_5= Image.objects.create(property=property,
                                        image=file['image_5'],
                                        title=form['image_5_title'])
        property.images.add(image_5)

# only for hosts
def update_property(form,file,logged_in_user_id):
    property=Property.objects.get(id=form['id'])
    property.type=Type.objects.get(id=form['type'])
    property.rent_type=Rent_type.objects.get(id=form['rent_type'])
    property.area=form['area']
    property.elevator=form['elevator']
    property.rent_allowance=form['rent_allowance']
    property.num_bedrooms=form['num_bedrooms']
    property.num_living_rooms=form['num_living_rooms']
    property.num_kitchens=form['num_kitchens']
    property.num_balconies=form['num_balconies']
    property.num_bathrooms=form['num_bathrooms']
    property.num_air_conditions=form['num_air_conditions']
    property.num_parkings=form['num_parkings']
    property.internet_service=form['internet_service']
    property.city=City.objects.get(id=form['city'])
    property.address=form['address']
    property.is_vacant=form['is_vacant']
    if form['rent_start_date'] == '':
        property.rent_start_date = ''
    else:
        try:
            property.rent_start_date = datetime.datetime.strptime(form['rent_start_date'], '%Y-%m-%d').date()
        except ValueError:
            property.rent_start_date = '' 
    if form['rent_end_date'] == '':
        property.rent_end_date = ''
    else:
        try:
            property.rent_end_date = datetime.datetime.strptime(form['rent_end_date'], '%Y-%m-%d').date()
        except ValueError:
            property.rent_end_date = '' 
    property.notes_host=form['notes_host']
    property.notes_host_private=form['notes_host_private']   
    images_list=Image.objects.filter(property=property)  
    if len(file) != 0:
        print("MMMMM inside edit images")
        # if len(images_list[0].image) > 0:
        #     os.remove(images_list[0].image.path) 
        #     images_list[0].image=file['image_1'] 
        #     images_list[0].image.save()
            # print("MMMMM inside if len(images_list[0].image) > 0 ")
            # print(file['image_1'].url)
        if 'image_1' in file:
            if len(images_list) > 0:
                os.remove(images_list[0].image.path) 
                images_list[0].delete()
            image_1= Image.objects.create(property=property,
                                    image=file['image_1'],
                                    title=form['image_1_title'])
            property.images.add(image_1)

        if 'image_2' in file:
            if len(images_list) > 1:
                os.remove(images_list[1].image.path) 
                images_list[1].delete()
            image_2= Image.objects.create(property=property,
                                    image=file['image_2'],
                                    title=form['image_2_title'])
            property.images.add(image_2)
            
        if 'image_3' in file:
            if len(images_list) > 2:
                os.remove(images_list[2].image.path) 
                images_list[2].delete()
            image_3= Image.objects.create(property=property,
                                    image=file['image_3'],
                                    title=form['image_3_title'])
            property.images.add(image_3)

        if 'image_4' in file:
            if len(images_list) > 3:
                os.remove(images_list[3].image.path) 
                images_list[3].delete()
            image_4= Image.objects.create(property=property,
                                    image=file['image_4'],
                                    title=form['image_4_title'])
            property.images.add(image_4)
            
        if 'image_5' in file:
            if len(images_list) > 4:
                os.remove(images_list[4].image.path) 
                images_list[4].delete()
            image_5= Image.objects.create(property=property,
                                    image=file['image_5'],
                                    title=form['image_5_title'])
            property.images.add(image_5)

    # this  condition is for admins only
    # only admins can change status of vehicles
    user_list=User.objects.filter(id=logged_in_user_id)
    user=user_list[0]
    if user:
        if user.role.title=='admin':
            if form['is_active']:
                property.is_active=form['is_active']
    property.save()
    
def delete_property(id):
    property=Property.objects.get(id=id)
    property.delete()

def all_properties_list():
        return Property.objects.all().order_by("created_at")
    
class Request_Manager(models.Manager):
    def make_request_validator(self,postData):
        errors={}
        
        start_date=postData.get('start_date')
        end_date=postData.get('end_date')
            
        if len(start_date)==0:
            errors["start_date"]="Rent start date should be selected"
        else:
            current_datetime =datetime.datetime.now()
            start_date_object = datetime.datetime.strptime(postData['start_date'], "%Y-%m-%d")
            if  start_date_object < current_datetime:
                errors["start_date"]="Rent start date should be after current date"
        if len(end_date)==0:
            errors["end_date"]="Rent end date should be selected"
        else:
            current_datetime =datetime.datetime.now()
            end_date_object = datetime.datetime.strptime(postData['end_date'], "%Y-%m-%d")
            if  end_date_object < current_datetime:
                errors["end_date"]="Rent end date should be after current date"
        if start_date and end_date:
            start_date_object = datetime.datetime.strptime(postData['start_date'], "%Y-%m-%d")
            end_date_object = datetime.datetime.strptime(postData['end_date'], "%Y-%m-%d")
            if start_date > end_date:
                errors["end_date"]="Rent end date should be after start date"
        return errors
    
class Request(models.Model):
    guest=models.ForeignKey(User,related_name='requests',on_delete=models.CASCADE)
    property=models.ForeignKey(Property,related_name='requests',on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()
    notes_guest=models.TextField(blank=True, null=True)
    notes_host=models.TextField(blank=True, null=True)
    notes_host_private=models.TextField(blank=True, null=True)
    notes_admin=models.TextField(blank=True, null=True)
    status=models.CharField(max_length=15)
    approved_by=models.ForeignKey(User,related_name='approved_requests',on_delete=models.CASCADE,null=True)
    rejected_by=models.ForeignKey(User,related_name='rejected_requests',on_delete=models.CASCADE,null=True)
    cancelled_by=models.ForeignKey(User,related_name='canceled_requests',on_delete=models.CASCADE,null=True)
    finished_by=models.ForeignKey(User,related_name='finished_requests',on_delete=models.CASCADE,null=True)
    approved_at=models.DateTimeField(null=True, blank=True)
    rejected_at=models.DateTimeField(null=True, blank=True)
    cancelled_at=models.DateTimeField(null=True, blank=True)
    finished_at=models.DateTimeField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=Request_Manager()

class Image(models.Model):
    property=models.ForeignKey(Property,related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/',default='uploads/default_image.jpg',null=True,blank=True)
    title = models.CharField(max_length=255)
    order=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class Type(models.Model):
    title=models.CharField(max_length=15)
    
class Rent_type(models.Model):
    title=models.CharField(max_length=15)
    
class City(models.Model):
    title=models.CharField(max_length=10)
    
class Role(models.Model):
    title=models.CharField(max_length=10)