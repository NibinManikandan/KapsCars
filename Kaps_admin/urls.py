from django.urls import path
from . import views

urlpatterns = [
    path('Kaps_admin/', views.Kaps_admin, name='Kaps_admin'),
    path('pro_management/', views.pro_management, name='pro_management'),
    path('crm/', views.crm, name='crm'),
    path('sell_car/', views.sell_car, name='sell_car'),
    path('users/', views.users, name='users'),
    path('delete_user/<str:id>/', views.delete_user, name='delete_user'),
    path('proposal/', views.proposal, name='proposal'),
    path('delete_proposel/<str:id>/', views.delete_proposel, name='delete_proposel'),
    path('add_product/', views.add_product, name='add_product'),
    path('delete_car/<str:id>/', views.delete_car, name='delete_car'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('search/', views.search_cars, name='search_cars'),
    path('Car_brands/', views.Car_brands, name='Car_brands'),
    path('add_brands/', views.add_brands, name='add_brands'),
    path('delete_brand/<str:id>/', views.delete_brand, name='delete_brand'),
    path('notification/', views.notification, name='notification'),
    path('dele_notification/<str:i>/<int:id>/', views.dele_notification, name='dele_notification'),
    path('career_data/', views.career_data, name='career_data'),
    path('add_careers/', views.add_careers, name='add_careers'),
    path('del_careers/<str:id>/', views.del_careers, name='del_careers'),
    path('add_happy_club/', views.add_happy_club, name='add_happy_club')   
]