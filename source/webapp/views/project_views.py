from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.http import urlencode
from django.views import View

from webapp.forms import ProjectForm, SimpleSearchForm
from webapp.models import Project
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView



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
        project_users = User.objects.filter(team__project_key=self.object).distinct()
        context['project_team'] = project_users
        return context

class ProjectCreateView(CreateView):
    model = Project
    template_name = 'project/create.html'
    form_class = ProjectForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'project/update.html'
    form_class = ProjectForm
    context_object_name = 'project'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    pk_kwargs_url = 'pk'
    template_name = 'project/delete.html'
    context_object_name = 'project'
    success_url = reverse_lazy('webapp:projects_view')


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

