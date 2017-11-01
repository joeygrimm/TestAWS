# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..login.models import User
from django.db import models

# Create your models here.
class ItemManager(models.Manager):
    def CreateItem(self,PostData, user_id):
        errors=[]
        creator_name= None
        product_name=PostData['new_item']
        if len(PostData['new_item']) < 3:
            errors.append("Please fillout the name of the item.")
        if user_id < 1:
            errors.append("User id is blank.")
        if Item.objects.filter(name=product_name).exists():
            errors.append("An item with this name exists.")
        if not errors:
            creator_name=User.objects.get(id=user_id)
            created_item=Item.objects.create(
                name=PostData['new_item'],
                created_by=creator_name,
            )
            created_item.users.add(creator_name)
            print ("You created {}!").format(self.name)
            return created_item
        return errors

    def AddItem(self, PostData, user_id):
        added_item= None
        errors=[]
        if PostData['list_item_add'] < 1:
            errors.append("Your Item ID is blank.")
        if user_id < 1:
            errors.append("User ID is blank.")
        if not errors:
            added_item=Item.objects.get(id=PostData['list_item_add'])
            added_user=User.objects.get(id = user_id)
            added_item.users.add(added_user)
            print("Added {} to item!").format(added_user)
            return
        return errors

class Item(models.Model):
    name=models.CharField(max_length=60)
    created_by=models.CharField(max_length=255)
    users=models.ManyToManyField(User)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=ItemManager()

    def __str__(self):
        return self.name
        