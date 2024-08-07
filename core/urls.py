from django.urls import path
from . import views

urlpatterns = [
    #index
    path('', views.home, name='home'),
    path('futured_cars/<str:id>/', views.futured_cars, name='futured_car'),

    #products -car
    path('collections/', views.collections, name='collections'),
    path('filter/', views.filter, name='filter'),
    path('car_details/<str:id>/', views.car_details, name='car_details'),

    #kaps_assured
    path('kaps_assured/', views.kaps_assured, name='kaps_assured'),

    #about us
    path('about_us/', views.about_us, name='about_us'),

    #emi
    path('emi/', views.emi, name='emi'),
    
    #login
    path('login/',views.user_login, name='login'),
    path('otp/', views.otp_verification , name='otp'),
    path('logout/', views.logout, name='logout'),

    
    # happiness club
    path('happiness_club_view/', views.happiness_club_view, name='happiness_club_view'),

    # careers
    path('careers/', views.careers, name='career_list'),

    # find a car
    path('find_a_car/', views.find_a_car, name='find_a_car'),

    # sell your car
    path('sell_a_car/', views.sell_a_car, name='sell_a_car'),
    path('proposal-success/', views.proposal_success, name='proposal_success'),

    path('test_drive/<int:id>', views.test_drive, name='test_drive'),
    path('book_now/<int:id>', views.book_now, name='book_now'),    

    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
]
