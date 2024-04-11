from django.db import models

# Create your models here.
class Users(models.Model):
    name=models.CharField(max_length=25)
    email=models.CharField(max_length=25)
    createpassword=models.CharField(max_length=25)
    Phonenumber=models.BigIntegerField()
    age=models.IntegerField()
    gender=models.CharField(max_length=25)
    place=models.CharField(max_length=25)
class Bookings(models.Model):
    STATUSCHOICES=(
        ('pending','Pending'),
        ('success','Success'),
        ('failed','Failed'),
    )
    Name=models.CharField(max_length=25)
    Doctor=models.CharField(max_length=25)
    Price=models.CharField(max_length=25)
    Cardno=models.CharField(max_length=25)
    Edate=models.CharField(max_length=25)
    Cvv=models.CharField(max_length=25)
    status=models.CharField(max_length=25,choices=STATUSCHOICES,default='pending')

