from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest,HttpResponse
from django.utils import timezone
from .models import Match
from django.shortcuts import render
from django.db.models import Q



def matches_page(request:HttpRequest):
    live_matches = (Match.objects.filter(status=Match.Status.LIVE).select_related("home_team", "away_team", "stadium").order_by("start_datetime"))
    upcoming_matches = (Match.objects.filter(status=Match.Status.UPCOMING, start_datetime__gte=timezone.now()).select_related("home_team", "away_team", "stadium").order_by("start_datetime"))
    featured_match = upcoming_matches.first()

    context = {
        "live_matches": live_matches,
        "upcoming_matches": upcoming_matches,
        "featured_match": featured_match,
    }

    return render(request, "match/match_page.html", context)


def match_detail(request, match_id:HttpRequest):
    match = get_object_or_404(Match.objects.select_related("home_team","away_team","stadium",),id=match_id)

    related_matches = Match.objects.filter(Q(home_team=match.home_team) |Q(away_team=match.home_team) |Q(home_team=match.away_team) |Q(away_team=match.away_team)).exclude(id=match.id).select_related(
        "home_team",
        "away_team",
        "stadium",
    )[:3]

    context = {
        "match": match,
        "related_matches": related_matches,
    }

    return render(request, "match/match_detail.html", context)

