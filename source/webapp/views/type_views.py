from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from webapp.forms import TypeForm

from webapp.models import Type
from django.views.generic import CreateView, UpdateView, DeleteView
from .base_views import ListView


class TypesView(ListView):
    template_name = 'type/types.html'
    model = Type
    context_key = 'types'


class TypeCreateView(CreateView):
    model = Type
    template_name = 'type/create_type.html'
    form_class = TypeForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:types_view')


class TypeUpdateView(LoginRequiredMixin, UpdateView):
    model = Type
    template_name = 'type/type_update.html'
    form_class = TypeForm
    context_object_name = 'type'

    def get_success_url(self):
        return reverse('webapp:types_view')


class TypeDeleteView(LoginRequiredMixin, DeleteView):
    model = Type
    template_name = 'type/type_delete.html'
    context_object_name = 'type'
    pk_kwargs_url = 'pk'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get(self.pk_kwargs_url)
        obj = get_object_or_404(self.model, pk=pk)
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            return redirect('webapp:types_view')
        except:
            return render(request, 'error_type.html')

