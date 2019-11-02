from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, Team


class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ['avatar', 'about_user', 'git_profile']


class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline]


class TeamAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user_key', 'project_key', 'started_at', 'ended_at']
    fields = ['user_key', 'project_key', 'started_at', 'ended_at']
    labels = {'user_key': 'User', 'project_key': 'Project', 'started_at': 'Started at', 'ended_at': 'Ended at'}


admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Team, TeamAdmin)