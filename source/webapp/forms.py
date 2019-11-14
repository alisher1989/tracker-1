from django import forms
from accounts.models import Team
from webapp.models import Status, Type, Task, Project

from django.contrib.auth.models import User


class TeamForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ['project_key', 'user_key', 'started_at', 'ended_at']


class ProjectForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.all_users = kwargs.pop('project_users')
        super().__init__(*args, **kwargs)
        self.fields['project_users'] = forms.ModelMultipleChoiceField(queryset=self.all_users, initial=self.initial.get('team'))

    class Meta:
        model = Project
        fields = ['name', 'description', 'project_status']


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


class TeamUpdateForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['team_users'] = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                                                   initial=self.initial.get('team'))
