# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import User
from django.contrib import messages
from django.shortcuts import render, reverse, redirect, HttpResponseRedirect

# Create your views here.

def index(request):
    return render(request, "login/index.html")

def logging_in(request):
    login_attempt=User.objects.LoginValidator(request.POST)

    if type(login_attempt) == list:
        for errs in login_attempt:
            messages.error(request, errs)
        print ("error when logging in")
        return HttpResponseRedirect(reverse("login:index"))
    request.session['user_id'] = login_attempt.id
    messages.success(request, "You've logged in!")
    print "You logged in! You're Doing great"
    return redirect("/success")

def create(request):
    create_attempt=User.objects.RegistrationValidator(request.POST)
    if type(create_attempt) == list:
        for err in create_attempt:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = create_attempt.id
    messages.success(request, "You've registered.")
    print "You Created a user"
    return redirect("/success")

def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context={
        "user":User.objects.get(id=request.session['user_id'])
    }
    return HttpResponseRedirect(reverse("wish:index"), context)

def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')

