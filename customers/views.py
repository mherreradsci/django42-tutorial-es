from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import Customer
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)

from .forms import CustomerForm


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    fields = "__All__"

    def get_queryset(self, *args, **kwargs):
        qs = super(CustomerListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs


class CustomerCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    success_message = 'Customer "%(name)s" was created successfully'


class CustomerUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Customer
    success_message = 'Customer "%(name)s" was updated successfully'

    form_class = CustomerForm


class CustomerDetailViev(LoginRequiredMixin, DetailView):
    model = Customer
    fields = "__all__"


class CustomerDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Customer
    success_url = reverse_lazy("customers:list")
    success_message = 'Customer "%(name)s" was deleted successfully'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy("customers:list")
            return HttpResponseRedirect(url)
        else:
            return super(CustomerDeleteView, self).post(request, *args, **kwargs)

    def form_valid(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(CustomerDeleteView, self).delete(request, *args, **kwargs)
