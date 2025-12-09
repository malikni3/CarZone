from django.db import models
from django.contrib.auth.models import User

class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brands/', blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Car(models.Model):
    TRANSMISSION_CHOICES = (('Manual', 'Manual'), ('Automatic', 'Automatic'))
    CONDITION_CHOICES = (('New', 'New'), ('Used', 'Used'))

    title = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.IntegerField()
    mileage = models.IntegerField()
    color = models.CharField(max_length=50)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)

    image = models.ImageField(upload_to='cars/')
    description = models.TextField()

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Sold', 'Sold'),
        ('Rejected', 'Rejected')
    )

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    message = models.TextField(blank=True, default="I am interested in this car.")

    def __str__(self):
        return f"{self.buyer.username} wants {self.car.title}"