from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import MangoUsersModelForm
from .models import MangoUsersModel


class MangoUsersListView(ListView):
    model = MangoUsersModel
    template_name = 'mango/mangousers_list.html'
    context_object_name = 'mango_users'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context['total_users'] = queryset.count()
        context['distinct_titles'] = queryset.values('title').distinct().count()
        context['average_age'] = queryset.aggregate(avg=Avg('age'))['avg']
        return context


class MangoUsersDetailView(DetailView):
    model = MangoUsersModel
    template_name = 'mango/mangousers_detail.html'
    context_object_name = 'mango_user'


class MangoUsersCreateView(SuccessMessageMixin, CreateView):
    model = MangoUsersModel
    form_class = MangoUsersModelForm
    template_name = 'mango/mangousers_form.html'
    success_url = reverse_lazy('mango:mangousers_list')
    success_message = 'User "%(name)s" was created successfully.'


class MangoUsersUpdateView(SuccessMessageMixin, UpdateView):
    model = MangoUsersModel
    form_class = MangoUsersModelForm
    template_name = 'mango/mangousers_form.html'
    success_url = reverse_lazy('mango:mangousers_list')
    success_message = 'User "%(name)s" was updated successfully.'


class MangoUsersDeleteView(DeleteView):
    model = MangoUsersModel
    template_name = 'mango/mangousers_confirm_delete.html'
    context_object_name = 'mango_user'
    success_url = reverse_lazy('mango:mangousers_list')

    def form_valid(self, form):
        messages.success(self.request, f'User "{self.object.name}" was deleted successfully.')
        return super().form_valid(form)
###########