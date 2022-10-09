
from turtle import title
from django.db import models
from django.forms import CharField

# Create your models here.

class Property(models.Model):
    name= models.CharField(max_length=100)
    
    
class Properties(models.Model):
    Link=models.URLField()
    img=models.ImageField(upload_to='pics')
    title=models.CharField(max_length=100)
    totprice=models.IntegerField()
    ppsqft=models.IntegerField()
    Superarea=models.IntegerField()
    Carpetarea=models.IntegerField()
    ProjectName=models.CharField(max_length=50)
    Furnishedstatus=models.CharField(max_length=50)
    Overlooking=models.CharField(max_length=50)
    CornerProperty=models.IntegerField()
    Washrooms=models.IntegerField()
    Carparking=models.CharField(max_length=50)
    LEEDCertification=models.CharField(max_length=50)
    BuildingClass=models.CharField(max_length=50)
    Lifts=models.IntegerField()
    WaterAvailability=models.CharField(max_length=50)
    Address=models.CharField(max_length=50)
    

    
    
class sp(models.Model):
    address= models.CharField(max_length=200)
    mintotprice= models.IntegerField()
    maxtotprice=models.IntegerField()
    superarea=models.IntegerField()
    
class Sell(models.Model):
    Link=models.URLField()
    img=models.ImageField(upload_to='pics')
    title=models.CharField(max_length=200)
    totprice=models.IntegerField()
    Superarea=models.IntegerField()
    Carpetarea=models.IntegerField()
    ProjectName=models.CharField(max_length=200)
    Furnishedstatus=models.CharField(max_length=200)
    Overlooking=models.CharField(max_length=200)
    CornerProperty=models.IntegerField()
    Washrooms=models.IntegerField()
    Carparking=models.CharField(max_length=50)
    LEEDCertification=models.CharField(max_length=50)
    BuildingClass=models.CharField(max_length=50)
    ConstructionStatus=models.CharField(max_length=50)
    Address=models.CharField(max_length=500)
    
