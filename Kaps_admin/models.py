from django.db import models

# Create your models here.


class Crm_Profile(models.Model):
    seller_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    address = models.TextField(blank=True)
    staff_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seller_name} {self.staff_name}"
    
