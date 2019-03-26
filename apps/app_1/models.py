from __future__ import unicode_literals
from django.db import models
from datetime import datetime, timedelta
from django_fields import DefaultStaticImageField
import bcrypt
import re
from django import forms
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class DataManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least two characters."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least two characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Email address must be valid."
        elif len(User.objects.filter(email=postData["email"])) > 0:
            errors["email"] = "Email is already registered."
        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least eight characters."
        elif postData['password'] != postData['confirm']:
            errors["password"] = "Passwords must match."
        return errors
    def login_validator(self, postData):
        errors = {}
        if postData['email'] == "":
            errors['email'] = "Enter an email."
        if postData['password'] == "":
            errors['password'] = "Enter a password."
        else:
            user = User.objects.filter(email=postData['email'])
            if len(user) == 0:
                errors['email'] = "Email and/or password does not match"
            elif not bcrypt.checkpw(postData['password'].encode(), user.first().password.encode()):
                errors['email'] = "Email and/or password does not match"
        return errors
    def trip_validator(self, postData):
        errors = {}
        if len(postData['destination']) < 2:
            errors["destination"] = "Title should be at least two characters."
        if len(postData['description']) < 2:
            errors["description"] = "Details should be at least two characters."
        if postData["start_date"] == "":
            errors["start_date"] = "Start date can't be empty."
        else:
            start_date = datetime.strptime(postData["start_date"], "%Y-%m-%d")
            if start_date < datetime.now():
                errors["start_date"] = "The start date has to be in the future."
        if postData["end_date"] == "":
            errors["end_date"] = "End date can't be empty."
        else:
            start_date = datetime.strptime(postData["start_date"], "%Y-%m-%d")
            end_date = datetime.strptime(postData["end_date"], "%Y-%m-%d")
            if end_date < start_date:
                errors["end_date"] = "End date must be later than the start date."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DataManager()
    def __repr__(self):
        return f"<User object: {self.first_name} ({self.id})>"

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    image = DefaultStaticImageField(upload_to="trip_image", blank=True, default_image_path='app_1/images/noimg2.png')
    # image = models.ImageField(upload_to="trip_image", default = 'app_1/images/noimg.png')
    planner = models.ForeignKey(User, related_name="planned_trips", on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name="attending_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = DataManager()
    def __repr__(self):
        return f"<Trip object: {self.destination} ({self.id})>"