from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from django.utils.translation import gettext as _


def home_view(request:HttpRequest):
    featured_match = Match.objects.select_related("home_team","away_team","stadium").first()

    return render(request, "core/home.html", {
        "featured_match": featured_match,
    })

def about_view(request:HttpRequest):
    return render(request, 'core/about.html')

from match.models import Match

