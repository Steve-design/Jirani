from django.db import models
from __future__ import unicode_literals
import numpy as np
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from django.db.models.sql.datastructures import Join

class tags(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    def save_tags(self):
        self.save()

    def delete_tags(self):
        self.delete()

class Location(models.Model):
    name = models.CharField(max_length=30)

    def save_location(self):
        self.save()

    def delete_location(self):
        self.delete()

    def __str__(self):
        return self.name   

class Image(models.Model):
    image = models.ImageField(upload_to='picture/', )
    name = models.CharField(max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="images")
    description = models.TextField()
    location = models.ForeignKey(Location, null=True)
    tags = models.ManyToManyField(tags, blank=True)
    likes = models.IntegerField(default=0)
    comments = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def save_image(self):
        self.save()


@classmethod
    def delete_image_by_id(cls, id):
        pictures = cls.objects.filter(pk=id)
        pictures.delete()

    @classmethod
    def get_image_by_id(cls, id):
        pictures = cls.objects.get(pk=id)
        return pictures

    @classmethod
    def filter_by_tag(cls, tags):
        pictures = cls.objects.filter(tags=tags)
        return pictures

    @classmethod
    def filter_by_location(cls, location):
        pictures = cls.objects.filter(location=location)
        return pictures

    @classmethod
    def search_image(cls, search_term):
        pictures = cls.objects.filter(name__icontains=search_term)
        return pictures

    @classmethod
    def update_image(cls, id):
        pictures = cls.objects.filter(id=id).update(id=id)
        return pictures

    @classmethod
    def update_description(cls, id):
        pictures = cls.objects.filter(id=id).update(id=id)
        return pictures


class Neighbourhood(models.Model):
    CITY_CHOICES = (
        ('Mzalendo City', 'Mzalendo City'),
        ('New Mumias', 'New Mumias'),
        ('Kajiado WaterMills', 'Kajiado WaterMills'),
        ('Lower RockState', 'Lower RockState'),
        ('RockState', 'RockState'),
        ('Mwiki Ridge', 'Mwiki Ridge'),
        ('Sunton City', 'Sunton City'),
        ('Nairobi', 'Nairobi'),
        ('Mombasa', 'Mombasa'),
        ('Kisumu', 'Kisumu'),

    )

    neighbourhood_name = models.CharField(max_length=30)
    neighbourhood_location = models.CharField(choices=CITY_CHOICES, max_length=200 ,default=0, null=True, blank=True)
    population= models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.neighbourhood_name

    def save_neighbourhood(self):
        self.save()

    @classmethod
    def delete_neighbourhood_by_id(cls, id):
        neighbourhoods = cls.objects.filter(pk=id)
        neighbourhoods.delete()

    @classmethod
    def get_neighbourhood_by_id(cls, id):
        neighbourhoods = cls.objects.get(pk=id)
        return neighbourhoods

    @classmethod
    def filter_by_location(cls, location):
        neighbourhoods = cls.objects.filter(location=location)
        return neighbourhoods

    @classmethod
    def search_neighbourhood(cls, search_term):
        neighbourhoods = cls.objects.filter(neighbourhood_name__icontains=search_term)
        return neighbourhoods

    @classmethod
    def update_neighbourhood(cls, id):
        neighbourhoods = cls.objects.filter(id=id).update(id=id)
        return neighbourhoods

    @classmethod
    def update_neighbourhood(cls, id):
        neighbourhoods = cls.objects.filter(id=id).update(id=id)
        return neighbourhoods    

class Business(models.Model):
    business_name = models.CharField(max_length=30, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="business")
    neighbourhood_id = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE,related_name="neighbourhoodbusiness",null=True,blank=True)
    business_email_address = models.CharField(max_length=200, null = True)

    def __str__(self):
        return self.business_name


    def save_business(self):
        self.save()   

    @classmethod
    def delete_business_by_id(cls, id):
        businesses = cls.objects.filter(pk=id)
        businesses.delete()

    @classmethod
    def get_businesses_by_id(cls, id):
        businesses = cls.objects.get(pk=id)
        return businesses

    @classmethod
    def filter_by_location(cls, location):
        businesses = cls.objects.filter(location=location)
        return businesses

    @classmethod
    def search_businesses(cls, search_term):
        businesses = cls.objects.filter(business_name__icontains=search_term)
        return businesses

    @classmethod
    def update_business(cls, id):
        businesses = cls.objects.filter(id=id).update(id=id)
        return businesses

    @classmethod
    def update_business(cls, id):
        businesses = cls.objects.filter(id=id).update(id=id)
        return businesses

