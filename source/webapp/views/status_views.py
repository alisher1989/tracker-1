from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from webapp.forms import StatusForm

from webapp.models import Status, Type
from django.views.generic import CreateView, UpdateView, DeleteView
from .base_views import ListView


class StatusesView(ListView):
    template_name = 'status/statuses.html'
    model = Status
    context_key = 'statuses'


class StatusCreateView(CreateView):
    model = Status
    template_name = 'status/create_status.html'
    form_class = StatusForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:statuses_view')


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'status/status_update.html'
    form_class = StatusForm
    context_object_name = 'status'

    def get_success_url(self):
        return reverse('webapp:statuses_view')


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'status/status_delete.html'
    context_object_name = 'status'
    pk_kwargs_url = 'pk'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get(self.pk_kwargs_url)
        obj = get_object_or_404(self.model, pk=pk)
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return redirect('webapp:statuses_view')
        except:
            return render(request, 'error.html')
