from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views import View

from accounts.models import Team
from webapp.forms import ProjectForm, SimpleSearchForm, TeamUpdateForm
from webapp.models import Project
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView


class ProjectsView(ListView):
    template_name = 'project/list.html'
    context_object_name = 'projects'
    model = Project
    ordering = ['-created_at']
    paginate_by = 4
    paginate_orphans = 1

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(name__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class ProjectView(DetailView):
    template_name = 'project/project.html'
    context_object_name = 'project'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_users = Team.objects.filter(project_key=self.object, ended_at=None).distinct()
        context['project_team'] = project_users
        return context


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    model = Project
    template_name = 'project/create.html'
    form_class = ProjectForm
    permission_required = 'webapp.add_project'
    permission_denied_message = '403 Доступ запрещен'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project_users'] = User.objects.all()
        return kwargs

    def form_valid(self, form):
        users = form.cleaned_data.pop('project_users')
        current_user = self.request.user
        users_list = list(users)
        users_list.append(current_user)
        self.object = form.save()
        for user in users_list:
            Team.objects.create(user_key=user, project_key=self.object, started_at=datetime.now())
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    model = Project
    template_name = 'project/update.html'
    form_class = ProjectForm
    context_object_name = 'project'
    permission_required = 'webapp.change_project'

    def get_initial(self):
        initial = super().get_initial()
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        initial['team'] = User.objects.filter(team__project_key=self.project, team__ended_at=None)
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project_users'] = User.objects.all()
        return kwargs

    def form_valid(self, form):
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        cleaned_users = form.cleaned_data.pop('project_users')
        users_select = self.request.POST.getlist('project_users')
        teams = Team.objects.filter(project_key=self.project)
        user_team = []

        for pk in users_select:
            user = User.objects.get(pk=pk)
            user_team.append(user.username)

        for team in teams:
            if team.user_key.username in user_team:
                continue
            else:
                team.ended_at = datetime.now()
                team.save()

        for user in cleaned_users:
            user, _ = Team.objects.get_or_create(user_key=user, project_key=self.project, started_at=datetime.now(),
                                                 ended_at=None)

        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    model = Project
    pk_kwargs_url = 'pk'
    template_name = 'project/delete.html'
    context_object_name = 'project'
    success_url = reverse_lazy('webapp:projects_view')
    permission_required = 'webapp.delete_project'


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model = Team
    context_object_name = 'project'
    pk_kwargs_url = 'pk'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.ended_at = datetime.now()
        self.object.save()
        return redirect(reverse('webapp:project_view', kwargs={'pk': self.object.project_key.pk}))


class ProjectUsersUpdateView(LoginRequiredMixin, FormView):
    template_name = 'project/change_project_members.html'
    form_class = TeamUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        initial = super().get_initial()
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        initial['team'] = User.objects.filter(team__project_key=self.project, team__ended_at=None)
        return initial

    def form_valid(self, form):
        self.project = get_object_or_404(Project, pk=self.kwargs['pk'])
        cleaned_users = form.cleaned_data.pop('team_users')
        users_select = self.request.POST.getlist('team_users')
        teams = Team.objects.filter(project_key=self.project)
        user_team = []

        for pk in users_select:
            user = User.objects.get(pk=pk)
            user_team.append(user.username)

        for team in teams:
            if team.user_key.username in user_team:
                continue
            else:
                team.ended_at = datetime.now()
                team.save()

        for user in cleaned_users:
            user, _ = Team.objects.get_or_create(user_key=user, project_key=self.project, started_at=datetime.now(),
                                                     ended_at=None)

        return redirect(self.get_success_url())




    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.project.pk})

    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     project = self.get_object()
    #     return render(request, 'project/delete.html', context={'project': project})
    #
    # def post(self, request, *args, **kwargs):
    #     self.project = self.get_object()
    #     self.project.project_status = 'blocked'
    #     self.project.save()
    #     return redirect(self.get_redirect_url())
    #
    # def get_object(self):
    #     pk = self.kwargs.get(self.pk_kwargs_url)
    #     project = get_object_or_404(self.model, pk=pk)
    #     return project
    #
    # def get_redirect_url(self):
    #     return self.redirect_url

