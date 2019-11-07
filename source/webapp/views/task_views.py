from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode

from accounts.models import Team
from webapp.forms import TaskForm, SimpleSearchForm
from webapp.models import Task, Project
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class IndexView(ListView):
    template_name = 'task/index.html'
    context_object_name = 'tasks'
    model = Task
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
            query = Q(summary__icontains=self.search_value) | Q(description__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_search_form(self):
        return SimpleSearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data['search']
        return None


class TaskView(DetailView):
    template_name = 'task/task.html'
    context_object_name = 'task'
    model = Task


class TaskCreateView(CreateView):
    model = Task
    template_name = 'task/create.html'
    form_class = TaskForm
    pk_kwargs_url = 'pk'

    def get_queryset(self):
        project = get_object_or_404(Project, name=self.kwargs['pk'])
        print(project)
        return Task.objects.filter(project=project)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     print(self.kwargs['pk'])
    #     context['project'] = self.pk_kwargs_url
    #     return context

    # def get_form(self, **kwargs):
    #     if self.request.method == 'GET':
    #         form = TaskForm(user=self.request.user, instance=Task())
    #     else:
    #         form = TaskForm(user=self.request.user, instance=Task(), data=self.request.POST)
    #     return form

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        # users_project = Project.objects.filter(team__user_key=project.pk)
        kwargs['project'] = project
        return kwargs

    def form_valid(self, form):
        assigned_to = self.request.POST.get('assigned_to')
        user = User.objects.get(username=assigned_to)
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.assigned_to = user
        self.object.project = project
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        pk = self.kwargs.get(self.pk_kwargs_url)
        project = get_object_or_404(Project, pk=pk)
        for team in project.team.all():
            if self.request.user != team.user_key:
                return self.request.user == team.user_key
            return redirect('user_error.html')

    def get_success_url(self):
        return reverse('webapp:task_view', kwargs={'pk': self.object.pk})

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class=None)
    #     users_project = Project.objects.filter(team__user_key=self.request.user.pk, team__ended_at=None)
    #     form.fields['project'].queryset = users_project
    #     return form

#     def form_valid(self, form):
#         project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
#         task = project..create(**form.cleaned_data)
#         return redirect('webapp:project_view', pk=task.project.pk)

    # def post(self, request, *args, **kwargs):
    #     form = self.form_class()
    #     assigned_to = self.request.POST.get('assigned_to')
    #     user = User.objects.get(username=assigned_to)
    #     print(user.pk)
    #     form.fields['assigned_to'].queryset = user.pk
    #     return super().post(request, *args, **kwargs)

class TaskUpdateView(UserPassesTestMixin, UpdateView):
    model = Task
    template_name = 'task/update.html'
    form_class = TaskForm
    context_object_name = 'task'
    pk_kwargs_url = 'pk'

    def test_func(self):
        pk = self.kwargs.get(self.pk_kwargs_url)
        project = get_object_or_404(Project, pk=pk)
        for team in project.team.all():
            if self.request.user != team.user_key:
                return self.request.user == team.user_key
            return redirect('user_error.html')

    def get_success_url(self):
        return reverse('webapp:task_view', kwargs={'pk': self.object.pk})


class TaskDeleteView(UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'task/delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('webapp:index')
    pk_kwargs_url = 'pk'

    def test_func(self):
        task = self.get_object()
        pk = self.kwargs.get(self.pk_kwargs_url)
        project = get_object_or_404(Project, pk=pk)
        for team in project.team.all():
            if self.request.user != team.user_key:
                return self.request.user == team.user_key or \
                       task.created_by or self.request.user.is_superuser
            return redirect('user_error.html')

    # def dispatch(self, request, *args, **kwargs):
    #     pk = self.kwargs.get(self.pk_kwargs_url)
    #     project = get_object_or_404(Project, pk=pk)
    #     projects_user_ids = project.team.all().values_list('user_key_id', flat=True)
    #     if request.user.id in projects_user_ids:
    #         return reverse(request, self.template_name, kwargs={'pk': pk})
    #     else:
    #         return render(request, 'user_error.html')

    # def dispatch(self, request, *args, **kwargs):
    #     pk = self.kwargs.get(self.pk_kwargs_url)
    #     project = get_object_or_404(Project, pk=pk)
    #     for team in project.team.all():
    #         print(team)
    #         print(team.user_key)
    #         if request.user == team.user_key:
    #             return redirect('webapp:project_update', pk=pk)
    #         return render(request, 'user_error.html')


   #
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset

    # def get_users(self):
    #     pk = self.kwargs.get(self.pk_kwargs_url)
    #     project = get_object_or_404(Project, pk=pk)
    #     for user in project.team.all():
    #         print(user)

    # def get(self, request, *args, **kwargs):
    #     task = self.get_object()
    #     return render(request, 'task/update.html', context={'task': task})

    # def get_object(self, *args, **kwargs):
    #     pk = self.kwargs.get(self.pk_kwargs_url)
    #     task = get_object_or_404(self.model, pk=pk)
    #     return task

    # def get_project(self, *args, **kwargs):
    #     pk = self.kwargs.get(self.pk_kwargs_url)
    #     project = get_object_or_404(Project, pk=pk)
    #     return project

    # def get_redirect_url(self):
    #     return self.get_redirect_url

    #
    # def form_valid(self, form):
    #     for task in self.get_project().projects_task.all:
    #         print(task)
