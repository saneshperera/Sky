# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Team

#this will get the search text from the search bar, if the user hasnt searched anything, then it stays empty
def team_list(request):
    query = request.GET.get('q', '')
#this will get all the teams from the database and order them by the team name
    teams = Team.objects.all().order_by('team_name')

    if query:
        teams = teams.filter(
            Q(team_name__icontains=query) |
            Q(department__icontains=query) |
            Q(team_leader__icontains=query) |
            Q(skills__icontains=query) |
            Q(members__full_name__icontains=query) |
            Q(members__role__icontains=query)
        ).distinct()
#the teams and the search text will be sent to the HTML page
    context = {
        'teams': teams,
        'query': query,
    }

    return render(request, 'teams/team_list.html', context)

#this will find the selected team by using its ID
#if django cannot find the team, error code 404 will display
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
#this will send the selected team to the detail page
    context = {
        'team': team,
    }

    return render(request, 'teams/team_detail.html', context)


def organisation(request):
    #this will get the selected team from the dropdown menu
    selected_team_id = request.GET.get('team')
    #this will get all teams so they can be displayed in the dropdown
    teams = Team.objects.all().order_by('team_name')

#until a team is selected, these will start empty
    selected_team = None
    upstream_teams = []
    downstream_teams = []
#this will find the selected team from the database
    if selected_team_id:
        selected_team = get_object_or_404(Team, id=selected_team_id)

        #thiss will get the downstream dependency names from the selected team and should be split by commas as they are stored as text.
        downstream_names = [
            name.strip()
            for name in selected_team.downstream_dependencies.split(',')
            if name.strip()
        ]
#this should match every downstream dependency to a team in the database
        for name in downstream_names:
            match = Team.objects.filter(team_name__icontains=name).first()
            if match:
                downstream_teams.append(match)

        #this should calculate the upstream teams. if another team has the selected team as downstream, then that team is the upstream of the selected team
        possible_upstream_teams = Team.objects.exclude(id=selected_team.id)

        for team in possible_upstream_teams:
            listed_dependencies = [
                name.strip().lower()
                for name in team.downstream_dependencies.split(',')
                if name.strip()
            ]

            selected_team_name = selected_team.team_name.lower()

            if selected_team_name in listed_dependencies:
                upstream_teams.append(team)
                
#this should send all the organisation data to the HTML page
    context = {
        'teams': teams,
        'selected_team': selected_team,
        'upstream_teams': upstream_teams,
        'downstream_teams': downstream_teams,
    }

    return render(request, 'teams/organisation.html', context)