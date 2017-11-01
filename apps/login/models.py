# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import datetime
import bcrypt
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')


# Create your models here.

class UserManager(models.Manager):
    def RegistrationValidator(self,PostData):
        errors =[]
         
        for key, value in PostData.iteritems():
            if len(value) < 1:
                errors.append("Please fillout all fields to register.")
                break

        if len(PostData['first_name']) < 2 or len(PostData['last_name']) < 2:
            errors.append("Please fill out your first and last name.")
            
        if not re.match(NAME_REGEX, PostData['first_name']) or not re.match(NAME_REGEX, PostData['last_name']):
            errors.append('Your first and last name can not contain special charaters or numbers.')

        if not re.match(EMAIL_REGEX, PostData['email']):
            errors.append('Please enter a valid email address.')
        
        if len(PostData['password']) < 8:
            errors.append("Your password must be at least 8 characters in length.")
        
        if len(PostData['password']) != len(PostData['confpassword']):
            errors.append('Your password and password confirmation do not match.')

        if not errors:
            hashed = bcrypt.hashpw((PostData['password'].encode()), bcrypt.gensalt(5))

            new_user = User.objects.create(
                first_name=PostData['first_name'],
                last_name=PostData['last_name'],
                user_name=PostData['user_name'],
                email=PostData['email'],
                password = hashed,
                hire_date=PostData['hiredate']
            )
            return new_user
        return errors

    def LoginValidator(self,PostData):
        errors=[]
        
        if len(self.filter(email=PostData['email'])) > 0:
            
            user = self.filter(email=PostData['email'])[0]
            if not bcrypt.checkpw(PostData['password'].encode(), user.password.encode()):
                errors.append('Email or password is incorrect.')

        else:
            errors.append('Email or password is incorrect.')

        if errors:
            return errors

        return user

        

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    user_name=models.CharField(max_length=255)
    email=models.EmailField()
    password=models.CharField(max_length=255)
    hire_date=models.DateField(default=datetime.date.today)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserManager()

    def __str__(self):
        return self.user_name