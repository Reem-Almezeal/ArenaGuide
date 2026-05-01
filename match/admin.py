from django.contrib import admin
from .models import Team, Player, Match


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "coach", "founded_year")
    list_filter = ("country",)
    search_fields = ("name", "country", "coach")
    ordering = ("name",)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "team", "number", "position", "nationality")
    list_filter = ("team", "position", "nationality")
    search_fields = ("name", "team__name", "position")
    ordering = ("team", "number")


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "home_team",
        "away_team",
        "stadium",
        "start_datetime",
        "status",
        "available_tickets",
    )
    list_filter = ("status", "stadium", "start_datetime")
    search_fields = (
        "home_team__name",
        "away_team__name",
        "stadium__name",
    )
    ordering = ("-start_datetime",)
    list_editable = ("status", "available_tickets")
