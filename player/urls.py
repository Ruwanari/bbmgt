from django.urls import path
from . import views

urlpatterns = [
    path("team/player/<int:id>",views.getPlayer, name="index"),
    path("team/<int:id>",views.getTeam, name="index"),
    path("team/<int:id>/best", views.getBest, name="index"),
    path("",views.getOverview),
]