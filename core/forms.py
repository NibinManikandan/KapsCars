from django import forms
from .models import SellYourCar

class SellYourCarForm(forms.ModelForm):
    class Meta:
        model = SellYourCar
        fields = [
            'car_reg_number', 'brand_name', 'car_model', 
            'registered_year', 'fuel_type', 'km_driven', 
            'selling_price', 'images'
        ]
        widgets = {
            'car_reg_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Car Registration Number',
                'id': 'carRegNumber'
            }),
            'brand_name': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select Your Brand',
                'id': 'carBrand'
            }),
            'car_model': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select Your Model',
                'id': 'carModel'
            }),
            'registered_year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Registered Year',
                'id': 'registeredYear'
            }),
            'fuel_type': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select Fuel Type',
                'id': 'fuelType'
            }),
            'km_driven': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'KM Driven',
                'id': 'kmDriven'
            }),
            'selling_price': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Selling Price',
                'id': 'sellingPrice'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
                'id': 'carImage',
                'multiple': False
            }),
        }
