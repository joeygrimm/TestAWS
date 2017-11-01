# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from .models import Item
from ..login.models import User
from django.shortcuts import render, reverse, HttpResponseRedirect, redirect

# Create your views here.

def index(request):
    currentuser=User.objects.get(id=request.session['user_id'])
    notuser=User.objects.all().exclude(id=request.session['user_id'])

    context={
        "your_items":Item.objects.filter(users__pk=request.session['user_id']),
        "other_items":Item.objects.all().exclude(users__pk=request.session['user_id']),
        "currentuser":currentuser,
    }
    return render(request, "wish_items/index.html", context)

def itemcreate(request):

    return render( request, "wish_items/create.html")

def add(request):
    add_product=Item.objects.AddItem(request.POST, request.session['user_id'])
    if type(add_product)==list:
        for err in add_product:
            messages.error(request, err)
        return redirect("/wish_items/")
    messages.success(request, "You added a new item.")
    return redirect("/wish_items/")

def remove(request):
    deleted_item=Item.objects.get(id=request.POST['list_item_delete'])
    person_deleting=User.objects.get(id=request.session['user_id'])
    deleted_item.users.remove(person_deleting)
    messages.success(request,"You removed an item from your list.")
    return redirect("/wish_items/")

def show(request,item_id):
    context={
        "shown":Item.objects.get(pk=item_id)
    }
    return render(request, "wish_items/show.html", context)

def new(request):
    create_product=Item.objects.CreateItem(request.POST, request.session['user_id'])
    if type(create_product)==list:
        for err in create_product:
            messages.error(request, err)
        return redirect("/wish_items/itemcreate")
    messages.success(request, "You created a new item.")
    return HttpResponseRedirect(reverse("wish:index"))
    
def delete(request):
    erased_item=Item.objects.get(id=request.POST['erase_item']).created_by
    deleting_user=User.objects.get(id=request.session['user_id']).user_name

    if erased_item == deleting_user:
        erased_item.delete()
        messages.success(request,"You deleted your created item.")
    else:
        messages.error(request,"This cannot be deleted, since your not the item creator.")

    return redirect("/wish_items/")