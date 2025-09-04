from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Promoter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    area = models.CharField(max_length=30)
    phone = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    nationality = CountryField(blank_label='Choose a country', null=True)
    phone = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=30)
    promoter = models.ForeignKey(Promoter, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Table(models.Model):
    number = models.IntegerField(null=False, blank=False)
    capacity = models.IntegerField(null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
        
    def __str__(self):
        return f'{self.number}'


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=False)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, blank=False)
    guests = models.IntegerField(null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    promoter = models.ForeignKey(Promoter, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return