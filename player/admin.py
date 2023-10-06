from django.contrib import admin
from player.models import team, player, match, match_stats


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name']

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'height', 'teamId_id']

class MatchAdmin(admin.ModelAdmin):
    list_display = ['round', 'team1_id', 'team2_id']


admin.site.register(team, TeamAdmin)
admin.site.register(player, PlayerAdmin)