from django.db import models

class Team(models.Model):
    team_name = models.CharField(max_length=200)
    department = models.CharField(max_length=200, blank=True)
    team_leader = models.CharField(max_length=200, blank=True)
    department_head = models.CharField(max_length=200, blank=True)
    team_type = models.CharField(max_length=100, blank=True)

    mission = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    skills = models.TextField(blank=True)

    contact_email = models.EmailField(blank=True)
    slack_channel = models.CharField(max_length=200, blank=True)

    code_repository = models.URLField(blank=True)
    jira_board = models.URLField(blank=True)
    wiki_page = models.URLField(blank=True)

    upstream_dependencies = models.TextField(blank=True)
    downstream_dependencies = models.TextField(blank=True)

    def __str__(self):
        return self.team_name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    full_name = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    skills = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.full_name