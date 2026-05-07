from django.urls import path
from . import views

app_name = "match"

urlpatterns = [
    path("", views.matches_page, name="matches"),
    path("matches/<int:match_id>/", views.match_detail, name="match_detail"),
]