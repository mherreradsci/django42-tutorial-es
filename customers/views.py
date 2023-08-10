from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q

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
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q")
        if query:
            loockups = Q(code__icontains=query) | Q(name__icontains=query)
            qs = Customer.objects.filter(loockups)
        else:
            qs = super(CustomerListView, self).get_queryset(*args, **kwargs)

        return qs.order_by("-id")

    def get_template_names(self):
        if self.request.htmx and not self.request.htmx.history_restore_request:
            return "customers/partials/customer_table.html"
        return "customers/customer_list.html"

    # def get_paginate_by(self, queryset):
    #     result = self.request.GET.get("paginate_by", self.paginate_by)
    #     return self.request.GET.get("paginate_by", self.paginate_by)


class CustomerCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    success_message = 'Customer "%(name)s" was created successfully'

    def get_initial(self):
        initial = super(CustomerCreateView, self).get_initial()
        initial["created_by"] = self.request.user
        initial["updated_by"] = self.request.user
        return initial

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.updated_by = self.request.user
        obj.save()
        return super(CustomerCreateView, self).form_valid(form)


class CustomerUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Customer
    success_message = 'Customer "%(name)s" was updated successfully'

    form_class = CustomerForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        # obj.created_by = self.request.user
        obj.updated_by = self.request.user
        obj.save()
        return super(CustomerUpdateView, self).form_valid(form)


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
