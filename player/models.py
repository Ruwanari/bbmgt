from django.db import models

# Create your models here.

class team(models.Model):
    name = models.CharField(max_length=200)
    coachName = models.CharField(max_length=500)

    def __str__(self):
        return self.name

class player(models.Model):
    name = models.CharField(max_length=500)
    height =models.IntegerField()
    teamId = models.ForeignKey(team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class match(models.Model):
    round = models.IntegerField()
    team1 = models.ForeignKey(team, related_name='team1_players', on_delete=models.CASCADE)
    team2 = models.ForeignKey(team, related_name='team2_players', on_delete=models.CASCADE)
    team1Score = models.IntegerField()
    team2Score = models.IntegerField()
    date = models.DateField()

class match_stats(models.Model):
    matchNumber =models.ForeignKey(match, on_delete=models.CASCADE)
    playerId = models.ForeignKey(player, on_delete=models.CASCADE)
    points = models.IntegerField()