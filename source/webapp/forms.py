from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from accounts.models import Team
from webapp.models import Status, Type, Task, Project

from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'project_status']


def get_object(self):
    pk = self.kwargs.get(self.pk_kwargs_url)
    project = get_object_or_404(Project, pk=pk)
    return project


class TaskForm(forms.ModelForm):
    def __init__(self, project, **kwargs):
        super().__init__(**kwargs)
        teams = Team.objects.filter(project_key=project)
        users = []
        for team in teams:
            users.append(team)
        self.fields['assigned_to'].queryset = User.objects.filter(
            username__in=users
        )

    # def clean_assigned_to(self):
    #     super().clean()
    #     assigned_to = self.cleaned_data.get('assigned_to')
    #     project = self.cleaned_data.get('project')
    #     print(project)
    #     try:
    #         User.objects.get(username=assigned_to)
    #         return assigned_to
    #     except User.DoesNotExist:
    #         raise ValidationError('Пользователь не существует!')

    class Meta:
        model = Task
        fields = ['summary', 'description', 'status', 'type', 'assigned_to']


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['status']


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['type']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Search')