from django.contrib import admin

# Register your models here.
from .models import Team, TeamMember


class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'department', 'team_leader', 'team_type')
    search_fields = ('team_name', 'department', 'team_leader', 'skills')
    inlines = [TeamMemberInline]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'team', 'role', 'email')
    search_fields = ('full_name', 'role', 'email', 'skills')