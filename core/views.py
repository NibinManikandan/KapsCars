from http.client import REQUESTED_RANGE_NOT_SATISFIABLE
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.conf import settings
import random
import requests
from django.contrib import messages
from .models import *
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
import json
from .forms import SellYourCarForm
from django.contrib.auth import login
from .models import UserLogin
import urllib.parse
from django.contrib.auth.models import User


# User Login 
def send_otp(mobile, otp):
    url = "https://www.fast2sms.com/dev/bulkV2"
    message = f"Welcome to KAPS! Your OTP is {otp}. Please enter this code to proceed. This OTP is valid for a few minutes."
    
    # URL encode the payload
    payload = {
        'sender_id': 'FSTSMS',
        'message': message,
        'route': 'p',
        'language': 'english',
        'numbers': mobile
    }
    encoded_payload = urllib.parse.urlencode(payload)
    
    headers = {
        'authorization': 'COPELWmYGZMgDi3TSFVAI19zUQJujk0x4eqtHrfcdwloX8sN5hkSylZhed7m6JDbp9MLif4UzXsjONga',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cache-Control': 'no-cache',
    }
    
    response = requests.post(url, data=encoded_payload, headers=headers)
    
    print(f"Sending OTP {otp} to {mobile}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")  # For debugging purposes
    
    if response.status_code == 200:
        try:
            response_data = response.json()
            print(f"Response JSON: {response_data}")
            if response_data.get('return'):
                print("OTP sent successfully.")
            else:
                print(f"Failed to send OTP: {response_data.get('message')}")
        except ValueError:
            print("Failed to parse JSON response.")
    else:
        print(f"Failed to send OTP. HTTP Status Code: {response.status_code}")


def user_login(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        
        # Generate a random 4-digit OTP
        otp = random.randint(1000, 9999)
        print(f"Generated OTP: {otp} for mobile: {mobile}")
        
        # Save user details and OTP in the session
        request.session['user_data'] = {
            'name': name,
            'email': email,
            'mobile': mobile,
            'otp': otp
        }
        
        # Send OTP to user's mobile number
        send_otp(mobile, otp)

        if not UserLogin.objects.filter(email=email).exists():
            user_obj=UserLogin(name=name,email=email,mobile=mobile)
            user_obj.save()
        
        # Redirect to OTP verification page
        return redirect('otp')
    
    # Check if the user is already logged in
    if 'is_logged_in' in request.session and request.session['is_logged_in']:
        return redirect('collections')
    
    return render(request, 'login.html')


from django.urls import reverse
def otp_verification(request):
    if request.method == 'POST':
        otp_1 = request.POST.get('otp_1')
        otp_2 = request.POST.get('otp_2')
        otp_3 = request.POST.get('otp_3')
        otp_4 = request.POST.get('otp_4')
        entered_otp = otp_1 + otp_2 + otp_3 + otp_4

        user_data = request.session.get('user_data')
        if not user_data:
            return HttpResponse("Session expired. Please login again.")
        
        stored_otp = str(user_data.get('otp'))
        print(f"Entered OTP: {entered_otp}, Stored OTP: {stored_otp}")
        
        if entered_otp == stored_otp:
            user, created = User.objects.get_or_create(
                username=user_data['email'],
                defaults={'email': user_data['email'], 'first_name': user_data['name'], 'last_name': ''},
            )
            
            user_obj = UserLogin.objects.get(email=user_data['email'])
            user_obj.is_active = True
            user_obj.save()
            request.session['is_logged_in'] = True
            login(request, user)
            
            # Debug statements to check session keys
            sell_car_key = request.session.get('sell_car_key')
            find_car_key = request.session.get('find_car_key')
            car_details_key = request.session.get('car_details')
            futured_car_key = request.session.get('car_details')
            
            
            
            if sell_car_key:
                del request.session['sell_car_key']
                return redirect(sell_car_key)
            
            if find_car_key:
                del request.session['find_car_key']
                return redirect(find_car_key)
            
            if car_details_key:
                return redirect(car_details_key)
            
            if futured_car_key:
                return redirect(futured_car_key)
            
            return redirect('home')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    
    return render(request, 'otp.html')



# logout
def logout(request):
    request.session.flush()
    return redirect('login')


# landing page
def home(request):
    futured_cars = Cars.objects.all()
    return render(request, 'index.html', {'futured_cars':futured_cars})



def futured_cars(request, id):
    if request.user.is_authenticated:    
        cars = Cars.objects.get(id=int(id))
        return render(request, 'car_details.html', {'cars':cars})
    else:
        request.session['car_details'] = request.path
        return redirect('login')
    


# find Your Car Form Submission
def find_a_car(request):
    if request.user.is_authenticated:
        fuel_choices = Fuel_type.objects.all().distinct()
        transmission_types = Transmission.objects.all().distinct()
        if request.method == 'POST':
            budget = request.POST.get('budget')
            fuel_type = request.POST.get('fuel')
            transmission = request.POST.get('transmission')

            budget_ranges = {
                '0-10': (0, 1000000),
                '10-20': (1000000, 2000000),
                '20-30': (2000000, 3000000),
                '30+': (3000000, float('inf'))
            }

            if budget != '30+':
                if budget in budget_ranges:
                    budget_min, budget_max = budget_ranges[budget]
                    filtered_cars = Cars.objects.filter(
                        fuel__Available_fuel_type=fuel_type,
                        transmission__Transmission_type=transmission,
                        price__gte=budget_min,
                        price__lte=budget_max if budget != '30+' else budget_min
                    )
                else:
                    filtered_cars = Cars.objects.none()
            else:
                filtered_cars = Cars.objects.filter(
                    fuel__Available_fuel_type=fuel_type,
                    transmission__Transmission_type=transmission,
                    price__gte=3000000,
                )

            return render(request, 'collections.html', {'cars':filtered_cars})

        context = {
            'fuel_choices': fuel_choices,
            'transmission_types': transmission_types
        }

        return render(request, 'find_car.html', context)
    else:
        request.session['find_car_key'] = 'find_a_car'
        
        return redirect('login')



from django.db.models import Q
# car collections
def collections(request):
    car_brand = Brand.objects.all().distinct()
    transmission_types = Transmission.objects.all().distinct()
    years = Cars.objects.values_list('reg_year', flat=True).distinct()
    data_set = Cars.objects.none()  # Initialize an empty queryset

    if request.method == 'POST':
        budget = request.POST.get('budget')
        year = request.POST.getlist('year')
        brand = request.POST.getlist('brand')
        transmission = request.POST.getlist('transmission')

        request.session['budget'] = budget
        if not budget:
            request.session['year'] = year
            request.session['brand'] = brand
            request.session['transmission'] = transmission

        budget = request.session.get('budget')
        year = request.session.get('year')
        brand = request.session.get('brand')
        transmission = request.session.get('transmission')

        budget_ranges = {
            '0-10': (0, 1000000),
            '10-20': (1000000, 2000000),
            '20-30': (2000000, 3000000),
            '30+': (3000000, float('inf'))
        }

        # Apply budget filter
        if budget and budget!='30+' and budget in budget_ranges:
            budget_min, budget_max = budget_ranges[budget]
            data_set = Cars.objects.filter(price__gte=budget_min, price__lte=budget_max)
        elif budget == '30+':
            data_set = Cars.objects.filter(price__gte=3000000)
        else:
            data_set = Cars.objects.all()  # No budget filter applied

        # Apply year filter
        if year:
            data_set = data_set.filter(reg_year__in=year)

        # Apply brand filter
        if brand:
            data_set = data_set.filter(brand__Available_brands__in=brand)

        # Apply transmission filter
        if transmission:
            data_set = data_set.filter(transmission__Transmission_type__in=transmission)

    else:
        data_set = Cars.objects.filter(is_listed=True)

    print(list(data_set))
    context = {
        'cars': list(data_set),
        'car_brand': car_brand,
        'transmission_types': transmission_types,
        'years': years
    }
    return render(request, 'collections.html', context)




# Sell Your Car
def sell_a_car(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            car_reg_number = request.POST.get('car_reg_number')
            car_brand = request.POST.get('car_brand')
            car_model = request.POST.get('car_model')
            registered_year = request.POST.get('registered_year')
            fuel_type = request.POST.get('fuel_type')
            km_driven = request.POST.get('km_driven')
            selling_price = request.POST.get('selling_price')
            images = request.FILES.get('images')

            brand = Brand.objects.get(Available_brands=car_brand)
            fuel = Fuel_type.objects.get(Available_fuel_type=fuel_type)
            user_obj = UserLogin.objects.get(email = request.user.email)
            sell=SellYourCar(
                car_reg_number=car_reg_number,
                brand_name=brand,
                car_model=car_model,
                registered_year=registered_year,
                fuel_type=fuel,
                km_driven=km_driven,
                selling_price=selling_price,
                images=images,
                proposed_user = user_obj,
                proposed_staff = None
            )

            sell.save()

            return redirect('proposal_success')

        car_brands = Brand.objects.all().distinct()
        car_fuel_types = Fuel_type.objects.all().distinct()

        context = {
            'car_brands': car_brands,
            'car_fuel_types': car_fuel_types,
        }
        return render(request, 'sell_a_car.html', context)
    else:
        request.session['sell_car_key'] = 'sell_a_car'
        return redirect('login')



# # Proposal Success 
def proposal_success(request):
    return render(request, 'proposal_success.html')



# Happiness Club 
def happiness_club_view(request):
    happiness_club_members = HappinessClub.objects.all()
    return render(request, 'happiness_club.html', {'happiness_club_members': happiness_club_members})
    



# Careers Page 
def careers(request):
    careers = Career.objects.all()
    return render(request, 'careers.html', {'careers': careers})

    

#kaps assured 
def kaps_assured(request):
    return render(request, 'kaps_assured.html')



#about us 
def about_us(request):
    return render(request, 'about_us.html')


#car details 
def car_details(request, id):
    if request.user.is_authenticated:
        cars = Cars.objects.get(id=int(id))
        image_list = Car_Image.objects.filter(car__id=cars.id).all()
        car_price = cars.price
        similar_cars = Cars.objects.filter(price__gte=car_price)
        
        context={
            'cars':cars,
            'car_images':image_list,
            'similar_cars':similar_cars,
            }
        return render(request, 'car_details.html', context)
    else:
        request.session['car_details'] = request.path
        return redirect('login')


#emi 
def emi(request):
    return render(request, 'emi.html')


from urllib.parse import urlencode
def filter(request):
    brands = Brand.objects.all().distinct()
    transmissions = Transmission.objects.all().distinct()
    years = Cars.objects.values_list('reg_year', flat=True).distinct()

    return render(request, 'filter_page.html', {
        'brands': brands,
        'transmission_types': transmissions,
        'years': sorted(years, reverse=True),
    })



# from django.urls import reverse
@login_required
def test_drive(request,id):
    cars = Cars.objects.get(id=id)
    user_obj = UserLogin.objects.get(email=request.user.email)
    if not Test_drive.objects.filter(car_data=cars,user_data =user_obj).exists():
        test_drive_obj = Test_drive(user_data=user_obj,car_data=cars)
        test_drive_obj.save()
    else:
        messages.error(request, 'You have already given submission for Test drive.')
        
        return redirect(f'../car_details/{id}/')
    return render(request, 'proposal_success.html')




@login_required
def book_now(request,id):
    cars = Cars.objects.get(id=id)
    user_obj = UserLogin.objects.get(email=request.user.email)
    if not Book_now.objects.filter(car_data=cars,user_data =user_obj).exists():
        test_drive_obj = Book_now(user_data=user_obj,car_data=cars)
        test_drive_obj.save()
    else:
        messages.error(request, 'You have already given submission for Booking.')
        
        return redirect(f'../car_details/{id}/')

    return render(request, 'proposal_success.html')
    



def privacy_policy(request):
    return render(request, 'privacy_policy.html')



def terms_and_conditions(request):
    return render(request, 'terms.html')