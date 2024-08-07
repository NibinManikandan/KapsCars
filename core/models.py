from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from Kaps_admin.models import Crm_Profile

# ==================== User Model (Customer) ======================
class UserLogin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ====================== Product Model (Car) =======================

class Brand(models.Model):
    Available_brands = models.CharField(max_length=50, blank=True, null=True)
    brand_description = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.Available_brands
    

class Fuel_type(models.Model):
    Available_fuel_type = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.Available_fuel_type


class Transmission(models.Model):
    Transmission_type = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.Transmission_type


class Cars(models.Model):
    brand = models.ForeignKey(Brand, null=False, on_delete=models.CASCADE, related_name='car_brand')
    fuel = models.ForeignKey(Fuel_type, null=False, on_delete=models.CASCADE, related_name='fueltype')
    model_name = models.CharField(max_length=50, blank=False, null=False)
    colour = models.CharField(max_length=20, blank=True, null=True)
    variant = models.CharField(max_length=20, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mileage = models.IntegerField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_listed = models.BooleanField(default=True)
    transmission = models.ForeignKey(Transmission, null=False, on_delete=models.CASCADE, related_name='trans_type')
    inspection_rating = models.IntegerField()
    reg_year = models.IntegerField()
    reg_month = models.CharField(max_length=10, blank=True, null=True)
    km_driven = models.IntegerField()
    rto = models.CharField(max_length=100)
    insurance_validity = models.DateField()
    insurance_type = models.CharField(max_length=20, blank=True, null=True)
    no_of_owners = models.CharField(max_length=100)
    finance_available = models.BooleanField(default=False)
    emi = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No')  # Add this line

    # ==================== inspection-related fields ========================
    engine_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    suspension_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    brakes_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    transmission_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    interior_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    wheels_tyres_rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)

    def __str__(self):
        return f"{self.reg_year} {self.model_name}"
    

class Car_Image(models.Model):
    car = models.ForeignKey(Cars, on_delete = models.CASCADE, related_name = 'images')
    Car_image = models.ImageField(upload_to='Car_images/',validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])])


    def __str__(self):
        return f'Image of {self.car.model_name}'


# ====================== Sell Your Car Model =============================
class SellYourCar(models.Model):
    car_reg_number = models.CharField(max_length=50)
    car_model = models.CharField(max_length=50, blank=True, null=True)
    registered_year = models.IntegerField()
    brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_name')
    fuel_type = models.ForeignKey(Fuel_type, on_delete=models.CASCADE, related_name='type_of_fuel')
    km_driven = models.IntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='sell_car_images/', blank=True, null=True)
    proposed_user = models.ForeignKey(UserLogin,on_delete=models.CASCADE,null=True,blank=False,related_name='selled_user')
    proposed_staff = models.ForeignKey(Crm_Profile,on_delete=models.CASCADE,null=True,blank=False,related_name='selled_staf')
    
    def __str__(self):
        return f"{self.brand_name.Available_brands} {self.car_model} - {self.car_reg_number}"


# ============================  careers ==============================
class Career(models.Model):
    job_title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField(max_length=254)
    date_posted = models.DateField(auto_now_add=True)
    last_date_to_apply = models.DateField()

    def __str__(self):
        return self.job_title

# ========================== Happines Club ============================
class HappinessClub(models.Model):
    owner_image = models.ImageField(upload_to='happiness_club/', blank=True,)
    testimonial = models.CharField(max_length=200)

    


class Test_drive(models.Model):
    user_data = models.ForeignKey(UserLogin, on_delete=models.CASCADE, related_name='user')
    car_data = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name='car')
    created_at = models.DateTimeField(auto_now_add=True)
    is_test = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.user_data.name} {self.car_data.model_name}"
    

class Book_now(models.Model):
    user_data = models.ForeignKey(UserLogin, on_delete=models.CASCADE, related_name='u_data')
    car_data = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name='c_data')
    created_at = models.DateTimeField(auto_now_add=True)
    is_test = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user_datas.name} {self.car_datas.model_name}"
    