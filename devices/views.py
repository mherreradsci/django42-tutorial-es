from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from .models import Device
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)

from .forms import DeviceForm, MacAddressFormset


class DeviceListView(LoginRequiredMixin, ListView):
    model = Device
    fields = "__All__"
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q")
        if query:
            loockups = Q(code__icontains=query) | Q(name__icontains=query)
            qs = Device.objects.filter(loockups)
        else:
            qs = super(DeviceListView, self).get_queryset(*args, **kwargs)

        return qs.order_by("-id")


class DeviceCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Device
    form_class = DeviceForm

    success_message = 'Device "%(name)s" was created successfully'

    def get_context_data(self, **kwargs):
        context = super(DeviceCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["macaddress_formset"] = MacAddressFormset(self.request.POST)
        else:
            context["macaddress_formset"] = MacAddressFormset()
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context["macaddress_formset"]

        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            instances = formset.save(commit=False)

            for instance in instances:
                instance.created_by = self.request.user
                instance.updated_by = self.request.user
                # instance.save()
            formset.save()
            return response
        else:
            return super().form_invalid(form)

    def get_initial(self):
        initial = super(DeviceCreateView, self).get_initial()
        initial["created_by"] = self.request.user
        initial["updated_by"] = self.request.user
        return initial


class DeviceUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Device
    success_message = 'Device "%(name)s" was updated successfully'

    form_class = DeviceForm

    def get_context_data(self, **kwargs):
        context = super(DeviceUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context["macaddress_formset"] = MacAddressFormset(
                self.request.POST, instance=self.object
            )
            context["macaddress_formset"].full_clean()
        else:
            context["macaddress_formset"] = MacAddressFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context["macaddress_formset"]
        if formset.is_valid():
            response = super().form_valid(form)
            formset.instance = self.object
            instances = formset.save(commit=False)
            for instance in instances:
                instance.updated_by = self.request.user
            formset.save()
            return response
        else:
            return super().form_invalid(form)


class DeviceDetailViev(LoginRequiredMixin, DetailView):
    model = Device


class DeviceDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Device
    success_url = reverse_lazy("devices:list")
    success_message = 'Device "%(name)s" was deleted successfully'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy("devices:list")
            return HttpResponseRedirect(url)
        else:
            return super(DeviceDeleteView, self).post(request, *args, **kwargs)

    def form_valid(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeviceDeleteView, self).delete(request, *args, **kwargs)
