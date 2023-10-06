from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import player, team, match, match_stats,coach
from django.db.models.functions import Coalesce
from django.db.models import F, ExpressionWrapper, FloatField, Sum, Count, Value
from collections import defaultdict
from django.contrib.auth.decorators import permission_required, login_required

@login_required
# @permission_required('player.view_player')
def getPlayer(request, id):
    isSuperUser = request.user.is_superuser
    email = request.user.email
    pl = player.objects.get(id=id)
    teamId = pl.teamId_id
    teamDetails = team.objects.get(id=teamId)
    coachDetails = coach.objects.get(id=teamDetails.coachId_id)
    if email == pl.email or email == coachDetails.email or isSuperUser == 1:
        count = match_stats.objects.filter(playerId_id=id).count()
        sum_result = match_stats.objects.filter(playerId_id=id).aggregate(total_sum=Sum('points'))['total_sum']
        avg_score = sum_result / count
        data = {
            'Name': pl.name,
            'Height': pl.height,
            'Number of matches played': count,
            'Average Score': avg_score
        }
        return JsonResponse(data)
    else:
        data = {
            'code': 500,
            'message': "You do not have access to this page!"

        }
        return JsonResponse(data)


@login_required# Create your views here.
# @permission_required('player.view_team')
def getTeam(request, id):
    isSuperUser = request.user.is_superuser
    email = request.user.email
    teamDetails = team.objects.get(id=id)
    coachDetails = coach.objects.get(id=teamDetails.coachId_id)
    if email == coachDetails.email or isSuperUser == 1:
        score_team_1 = match.objects.filter(team1_id=id).aggregate(total_sum1=Sum(Coalesce('team1Score', Value(0))))[
            'total_sum1']
        score_team_2 = match.objects.filter(team2_id=id).aggregate(total_sum2=Sum(Coalesce('team2Score', Value(0))))[
            'total_sum2']

        score_team_1 = score_team_1 or 0
        score_team_2 = score_team_2 or 0

        total_score = score_team_1 + score_team_2

        count_team_1 = match.objects.filter(team1_id=id).count()
        count_team_2 = match.objects.filter(team2_id=id).count()

        total_count = count_team_1 + count_team_2

        if total_count > 0:
            avg = total_score / total_count
        else:
            avg = 0  # Avoid division by zero

        plyerRows = player.objects.filter(teamId_id=id)

        name_list = []

        for pl in plyerRows:
            name = pl.name
            name_list.append(name)
        # Create a dictionary for the JSON response
        response_data = {'Average_Score_for_the_team': avg, 'Name_list': name_list}

        # Return the JSON response
        return JsonResponse(response_data)
    else:
        data = {
            'code': 500,
            'message': "You do not have access to this page!"

        }
        return JsonResponse(data)


def getOverview(request):
    matches = match.objects.all()

    match_stat_list = []

    for mat in matches:
        matchNp = mat.id
        round = mat.round
        team1 = team.objects.get(id=mat.team1_id)
        team2 = team.objects.get(id=mat.team2_id)
        team1Score = mat.team1Score
        team2Score = mat.team2Score
        if team1Score > team2Score:
            won = team.objects.get(id=team1.id)
        elif team2Score > team1Score:
            won = team.objects.get(id=team2.id)
        else:
            won = "Match was Drawn"

        new = {'round': round, 'match number': matchNp, 'team1': team1.name, 'team1 Score': team1Score, 'team2': team2.name, 'team2 Score': team2Score,
               'Winning team': won.name}

        match_stat_list.append(new)

    return JsonResponse(match_stat_list, safe=False)

@login_required
# @permission_required('player.view_team')
def getBest(request, id):
    isSuperUser = request.user.is_superuser
    email = request.user.email
    teamDetails = team.objects.get(id=id)
    coachDetails = coach.objects.get(id=teamDetails.coachId_id)
    if email == coachDetails.email or isSuperUser == 1:
        score_team_1 = match.objects.filter(team1_id=id).aggregate(total_sum1=Sum(Coalesce('team1Score', Value(0))))[
            'total_sum1']
        score_team_2 = match.objects.filter(team2_id=id).aggregate(total_sum2=Sum(Coalesce('team2Score', Value(0))))[
            'total_sum2']

        score_team_1 = score_team_1 or 0
        score_team_2 = score_team_2 or 0

        total_score = score_team_1 + score_team_2

        percentile = total_score * 90 / 100

        players_points = match_stats.objects.filter(playerId__teamId_id=id)

        # Create a dictionary to store the sum of points for each player
        player_points_sum = defaultdict(int)

        # Calculate the sum of points for each player
        for stat in players_points:
            player_id = stat.playerId_id
            points = stat.points
            player_points_sum[player_id] += points

        name_list = []
        for dictKey, dictValue in player_points_sum.items():
            if dictValue >= percentile:
                name_list.append(player.objects.get(id=dictKey).name)

        return JsonResponse(name_list, safe=False)
    else:
        data = {
            'code': 500,
            'message': "You do not have access to this page!"

        }
        return JsonResponse(data)
