from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


app_name='core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('logout/', LogoutView.as_view(next_page="home"), name="logout"),
]