from django.shortcuts import render,redirect,get_object_or_404
from core.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import user_passes_test

# Create your views here.


def Kaps_admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('pro_management')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        admin = authenticate(

            username=username,
            password=password
        )

        print(admin)

        if admin is not None and admin.is_superuser:
            login(request, admin)
            return redirect('pro_management')
        
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('Kaps_admin')

    return render(request, 'kaps_admin/admin_login.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def pro_management(request):
    Car_collections = Cars.objects.all().order_by('id')
    return render(request, 'kaps_admin/product_management.html', {'Car_collections':Car_collections})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def crm(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # CRM details
            seller_name = request.POST.get('seller')
            phone_num = request.POST.get('phone')
            email = request.POST.get('email')
            address = request.POST.get('address')
            staff_name = request.POST.get('staff')

            crm_obj = Crm_Profile(
                seller_name=seller_name,
                phone=phone_num,
                email=email,
                address=address,
                staff_name=staff_name
            )
            crm_obj.save()

            # Redirect to the same page to fill the car selling form
            return redirect('crm')

        car_brands = Brand.objects.all().distinct()
        car_fuel_types = Fuel_type.objects.all().distinct()

        context = {
            'car_brands': car_brands,
            'car_fuel_types': car_fuel_types,
        }
        return render(request, 'kaps_admin/crm.html', context)
    else:
        return redirect('Kaps_admin')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def sell_car(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Sell car details
            car_reg_number = request.POST.get('car_reg_number')
            car_brand = request.POST.get('car_brand')
            car_model = request.POST.get('car_model')
            registered_year = request.POST.get('registered_year')
            fuel_type = request.POST.get('fuel_type')
            km_driven = request.POST.get('km_driven')
            selling_price = request.POST.get('selling_price')
            images = request.FILES.get('images')

            crm_obj = Crm_Profile.objects.latest('id')
            brand = Brand.objects.get(Available_brands=car_brand)
            fuel = Fuel_type.objects.get(Available_fuel_type=fuel_type)
            sell = SellYourCar(
                car_reg_number=car_reg_number,
                brand_name=brand,
                car_model=car_model,
                registered_year=registered_year,
                fuel_type=fuel,
                km_driven=km_driven,
                selling_price=selling_price,
                images=images,
                proposed_user=None,
                proposed_staff=crm_obj
            )
            sell.save()

            return redirect('crm')

        car_brands = Brand.objects.all().distinct()
        car_fuel_types = Fuel_type.objects.all().distinct()

        context = {
            'car_brands': car_brands,
            'car_fuel_types': car_fuel_types,
        }
        return render(request, 'kaps_admin/sell_car.html', context)
    else:
        return redirect('Kaps_admin')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def delete_proposel(request,id):
    obj=SellYourCar.objects.get(id=int(id))
    profile_obj=None
    if obj.proposed_staff:
        profile_obj=obj.proposed_staff
    else:
        profile_obj=obj.proposed_user

    obj.delete()
    profile_obj.delete()

    return redirect('proposal')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def users(request):
    Users = UserLogin.objects.all().order_by('id')
    print(Users)
    return render(request, 'kaps_admin/users.html', {'Users':Users})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def delete_user(request, id):
    Users = get_object_or_404(UserLogin, id=id)
    Users.delete()
    return redirect('users')  # Redirect to a page that lists cars or a success page

    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def Car_brands(request):
    brands = Brand.objects.all().distinct()
    return render(request, 'kaps_admin/car_brands.html', {'brands':brands})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def add_brands(request):
    if request.method == 'POST':
        brand_name = request.POST.get('brand')
        description = request.POST.get('des')

        brand_obj = Brand(
            Available_brands = brand_name,
            brand_description = description
        )

        brand_obj.save()

        return redirect('Car_brands')

    return render(request, 'kaps_admin/add_brand.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def delete_brand(request, id):
    brands = get_object_or_404(Brand, id=id)
    brands.delete()
    return redirect('Car_brands')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def proposal(request):
    avail_proposals = SellYourCar.objects.all().order_by('id')
    return render(request, 'kaps_admin/proposal.html', {'avail_proposals':avail_proposals})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def add_product(request):
    Brand_choices = Brand.objects.all().distinct()
    transmission_choices = Transmission.objects.all().distinct()
    fuel_choices = Fuel_type.objects.all().distinct()
    if request.method == 'POST':
        Car_name = request.POST.get('brand')
        Car_model_name = request.POST.get('model_name')
        model = request.POST.get('model')
        variant = request.POST.get('variant')
        colour = request.POST.get('colour')
        Car_price = request.POST.get('price')
        Car_milage = request.POST.get('milage')
        Car_description = request.POST.get('description')
        transmission = request.POST.get('transmission')
        inspection = request.POST.get('inspection')
        Car_reg_year = request.POST.get('reg_year')
        Car_reg_month = request.POST.get('reg_month')
        km = request.POST.get('km')
        rto = request.POST.get('rto')
        insure_validity = request.POST.get('insure_validity')
        insure_type = request.POST.get('insure_type')
        owner = request.POST.get('owner')
        fuel = request.POST.get('fuel')
        emi = request.POST.get('emi')
        engine = request.POST.get('engine')
        suspension = request.POST.get('suspension')
        barke = request.POST.get('barke')
        transmission_rate = request.POST.get('transmission_rate')
        interior = request.POST.get('interior')
        wheels = request.POST.get('wheels')

        brand_obj=Brand.objects.get(Available_brands=Car_name)
        fuel_obj= Fuel_type.objects.get(Available_fuel_type=fuel)
        transmission_obj=Transmission.objects.get(Transmission_type=transmission)

        product = Cars(
            brand=brand_obj,
            model_name=Car_model_name,
            colour=colour,
            variant=variant,
            price=Car_price,
            mileage=Car_milage,
            transmission=transmission_obj,
            description=Car_description,
            inspection_rating=inspection,
            reg_year = Car_reg_year,
            reg_month = Car_reg_month,
            km_driven = km,
            rto = rto,
            insurance_validity = insure_validity,
            insurance_type = insure_type,
            no_of_owners = owner,
            fuel = fuel_obj,
            emi = emi,
            engine_rating = engine,
            suspension_rating = suspension,
            brakes_rating = barke,
            transmission_rating = transmission_rate,
            interior_rating = interior,
            wheels_tyres_rating = wheels
        )
        
        product.save()

        Car_images = request.FILES.getlist('images')
        for img in Car_images:
            Car_Image(car=product, Car_image=img).save()

        return redirect('pro_management')

    context = {
        'Brand_choices':Brand_choices,
        'transmission_choices':transmission_choices,
        'fuel_choices':fuel_choices
    }

    return render(request, 'kaps_admin/add_products.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def delete_car(request, id):
    cars = get_object_or_404(Cars, id=id)
    cars.delete()
    return redirect('pro_management') 
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def search_cars(request):
    search = request.GET.get('search', '')
    Car_collections = Cars.objects.filter(model_name__icontains=search)
    context = {
        'Car_collections': Car_collections,
    }
    return render(request, 'kaps_admin/product_management.html', context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def career_data(request):
    career_obj = Career.objects.all().distinct()
    return render(request, 'kaps_admin/careers_data.html', {'career_obj':career_obj})




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def add_careers(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        location = request.POST.get('location')
        exp = request.POST.get('exp')
        discription = request.POST.get('discription')
        email = request.POST.get('email')
        last_date = request.POST.get('last_date')


        careers = Career(
            job_title=title,
            location=location,
            experience=exp,
            description=discription,
            email=email,
            last_date_to_apply=last_date
        )
        careers.save()

        return redirect('career_data')
    
    return render(request, 'kaps_admin/add_careers.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def del_careers(request, id):
    career_obj = get_object_or_404(Career, id=id)
    career_obj.delete()
    return redirect('career_data')




from itertools import chain
from operator import attrgetter
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def notification(request):
    test_not = Test_drive.objects.all().order_by('id')
    book_not = Book_now.objects.all().order_by('id')
    notification_list = list(chain(test_not, book_not))
    notifications = sorted(notification_list, key=attrgetter('created_at'), reverse=True)
    
    return render(request, 'kaps_admin/notification.html', {'notifications':notifications})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def dele_notification(request,i, id):
    if i=='0':
        notification = get_object_or_404(Test_drive, id=id)
        notification.delete()
    elif i=='1':
        notification = get_object_or_404(Book_now, id=id)
        notification.delete()
    return redirect('notification')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def add_happy_club(request):
    if request.method == 'POST':
        images = request.FILES.get('images')
        testimonial = request.POST.get('testimonial')
        

        happiness_obj = HappinessClub(
            owner_image=images,
            testimonial=testimonial
        )

        happiness_obj.save()

        return redirect('add_happy_club')
    return render(request, 'kaps_admin/add_happy_club.html')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='Kaps_admin')
def admin_logout(request):
    request.session.flush()
    logout(request)
    return redirect('Kaps_admin')