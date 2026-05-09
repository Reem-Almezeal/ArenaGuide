from django.shortcuts import render
from django.http import HttpRequest,HttpResponse



def service_page(request:HttpRequest):
    return render(request, "service/services_page.html")