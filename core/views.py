from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from django.utils.translation import gettext as _
from match.models import Match
from django.contrib import messages
from .forms import ContactMessageForm


def home_view(request:HttpRequest):
    featured_match = Match.objects.select_related("home_team","away_team","stadium").first()

    return render(request, "core/home.html", {
        "featured_match": featured_match,
    })

def about_view(request:HttpRequest):
    return render(request, 'core/about.html')


def contact_page(request):

    if request.method == "POST":
        form = ContactMessageForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully.")
            return redirect("core:contact")
    else:
        form = ContactMessageForm()

    return render(request, "core/contact.html", {
        "form": form
    })




