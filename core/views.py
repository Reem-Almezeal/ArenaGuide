from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from django.utils.translation import gettext as _


def home_view(request:HttpRequest):
    return render(request, 'core/home.html')

def about_view(request:HttpRequest):
    return render(request, 'core/about.html')