from django.db import models
from django.contrib.auth.models import User
from django.forms import DateInput

# Create your models here.


class Restaurent(models.Model):
    name = models.CharField(max_length=40)
    restaurent_pics = models.ImageField(upload_to = 'restaurent_pics', blank=True)
    total_seat = models.IntegerField()
    opening = models.CharField(max_length=10)
    closed = models.CharField(max_length=10)
    location = models.CharField(max_length=200, default='')

    def __str__(self):
        return f'{self.name}'

TIME_CHOICES =(
    ("10", "10:00 AM"),
    ("11", "11:00 AM"),
    ("12", "12:00 PM"),
    ("1", "1:00 PM"),
    ("2", "2:00 PM"),

)

STATUS_CHOICES =(
    ("Pending", "Pending"),
    ("Accepted", "Accepted"),
    ("Rejected", "Rejected"),
    ("Restore", "Restore"),

)
class Reservation(models.Model):
    restaurents = models.ForeignKey(Restaurent, on_delete=models.CASCADE, null=False, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    person = models.IntegerField(default='1')
    booking_date = models.DateField(null=True)
    booking_time = models.CharField(choices=TIME_CHOICES, max_length=50, null=True)
    status = models.CharField(max_length=40,choices=STATUS_CHOICES,default='Pending')
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.restaurents.name} status {self.status}'

class Product(models.Model):
    restaurents = models.ForeignKey(Restaurent, on_delete=models.CASCADE, null=False, default='')
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images')
    price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    image = models.ImageField(upload_to="product_images")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurents = models.ForeignKey(Restaurent, on_delete=models.CASCADE, default='')
    service_type = models.CharField(max_length=100, null=True)
    tran_id = models.CharField(max_length=100, null=True)
    method = models.CharField(max_length=100, null=True)
   
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.restaurents.name

class History(models.Model):
    order_id = models.IntegerField(null=True)
    restaurent_name = models.CharField(max_length=100, null=True)
    restaurent_id = models.CharField(max_length=100, null=True)
    product_name = models.CharField(max_length=50, null=True)
    product_img = models.ImageField(upload_to="product_images", default="")
    product_id = models.CharField(max_length=50, null=True)
    price = models.CharField(max_length=50, null=True)
    quantity = models.CharField(max_length=50, null=True)
    service_type = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.product_name