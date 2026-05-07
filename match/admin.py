from django.contrib import admin
from .models import Team, Player, Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    
    list_display = ("match_name","stadium","start_datetime","status","home_score","away_score","live_minute","total_tickets","available_tickets","sold_tickets","sold_percentage",)
    list_filter = ("status", "stadium", "start_datetime")
    search_fields = ("home_team__name", "away_team__name", "stadium__name",)
    ordering = ("-start_datetime",)
    list_editable = ( "status", "home_score", "away_score", "live_minute", "available_tickets",)
    readonly_fields = ("sold_tickets","sold_percentage",)

    def match_name(self, obj):
        return f"{obj.home_team.name} vs {obj.away_team.name}"

    match_name.short_description = "Match"

    @admin.register(Team)
    class TeamAdmin(admin.ModelAdmin):
        list_display = ("name", "country", "coach", "founded_year")
        search_fields = ("name", "country", "coach")
        list_filter = ("country",)


    @admin.register(Player)
    class PlayerAdmin(admin.ModelAdmin):
        list_display = ("name", "team", "number", "position", "age", "nationality")
        search_fields = ("name", "team__name", "position", "nationality")
        list_filter = ("team", "position", "nationality")