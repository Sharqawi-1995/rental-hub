from django.db import models
import bcrypt
import re

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
    email=models.CharField(max_length=20, unique=True)
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
        rent_allowance=postData.get('rent_allowance')
        num_bedrooms=postData.get('num_bedrooms')
        num_living_rooms=postData.get('num_living_rooms')
        num_kitchens=postData.get('num_kitchens')
        num_balconies=postData.get('num_balconies')
        num_bathrooms=postData.get('num_bathrooms')
        num_air_conditions=postData.get('num_air_conditions')
        internet_service=postData.get('internet_service')
        city=postData.get('city')
        address=postData.get('address')
        is_active=postData.get('is_active')
        is_vacant=postData.get('is_vacant')
        notes=postData.get('notes')
        rent_start_date=postData.get('rent_start_date')
        rent_end_date=postData.get('rent_end_date')
        
        if len(type) == 0 :
            errors["type"]="Type should be selected"
        if len(rent_type) == 0 :
            errors["rent_type"]="Rent Type should be selected"
        if len(area) == 0 :
            errors["area"]="Area should be filled"
        if len(rent_allowance) == 0 :
            errors["rent_allowance"]="Rent allowence should be filled"
        if len(num_bedrooms) == 0 :
            errors["num_bedrooms"]="Number of bedrooms should be filled"
        if len(num_living_rooms) == 0 :
            errors["num_living_rooms"]="Number of living rooms should be filled"
        if len(num_kitchens) == 0 :
            errors["num_kitchens"]="Number of Kitchens should be filled"
        if len(num_balconies) == 0 :
            errors["num_balconies"]="Number of Balconies should be filled"
        if len(num_bathrooms) == 0 :
            errors["num_bathrooms"]="Number of bathrooms should be filled"
        if len(num_air_conditions) == 0 :
            errors["num_air_conditions"]="Number of air conditions should be filled"
        if len(internet_service) == 0 :
            errors["internet_service"]="Internet serivce should be selected"
        if len(city) == 0 :
            errors["city"]="City should be selected"
        if len(address) == 0 :
            errors["address"]="Address should be filled"
        if len(is_active) == 0 :
            errors["is_active"]="Is active should be selected"
        if len(is_vacant) == 0 :
            errors["is_vacant"]="Is vacant should be selected"
        return errors
            
class Property(models.Model):
    owner=models.ForeignKey(User,related_name="properties",on_delete=models.CASCADE)
    type=models.ForeignKey('Type',related_name="properties",on_delete=models.CASCADE,null=True)
    rent_type=models.ForeignKey('Rent_type',related_name="properties",on_delete=models.CASCADE,null=True)
    area=models.PositiveIntegerField(default=0)
    rent_allowance=models.PositiveIntegerField(default=0)
    num_bedrooms=models.PositiveIntegerField(default=0)
    num_living_rooms=models.PositiveIntegerField(default=0)
    num_kitchens=models.PositiveIntegerField(default=0)
    num_balconies=models.PositiveIntegerField(default=0)
    num_bathrooms=models.PositiveIntegerField(default=0)
    num_air_conditions=models.PositiveIntegerField(default=0)
    internet_service=models.BooleanField(default=False)
    city=models.ForeignKey('City',related_name="properties",on_delete=models.CASCADE,null=True)
    address=models.TextField(blank=True, null=True)
    is_active=models.BooleanField(default=False)
    is_vacant=models.BooleanField(default=False)
    rent_start_date=models.DateField()
    rent_end_date=models.DateField()
    notes=models.TextField(blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=Property_Manager()
    
def delete_property(id):
    property_list=Property.objects.filter(id=id)
    property=property_list[0]
    property.delete()

class Type(models.Model):
    title=models.CharField(max_length=15)
    
class Rent_type(models.Model):
    title=models.CharField(max_length=15)
    
class City(models.Model):
    title=models.CharField(max_length=10)
    
class Role(models.Model):
    title=models.CharField(max_length=10)
    
