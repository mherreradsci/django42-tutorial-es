from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from .models import Device
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)

from .forms import DeviceForm


class DeviceListView(LoginRequiredMixin, ListView):
    model = Device
    fields = "__All__"

    def get_queryset(self, *args, **kwargs):
        qs = super(DeviceListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs


class DeviceCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Device
    form_class = DeviceForm
    success_message = 'Device "%(name)s" was created successfully'

    def get_initial(self):
        initial = super(DeviceCreateView, self).get_initial()
        initial["created_by"] = self.request.user
        initial["updated_by"] = self.request.user
        return initial

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.updated_by = self.request.user
        obj.save()
        return super(DeviceCreateView, self).form_valid(form)


class DeviceUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Device
    success_message = 'Device "%(name)s" was updated successfully'

    form_class = DeviceForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.updated_by = self.request.user
        obj.save()
        return super(DeviceUpdateView, self).form_valid(form)


class DeviceDetailViev(LoginRequiredMixin, DetailView):
    model = Device
    fields = "__all__"


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
