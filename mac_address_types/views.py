from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from .models import MacAddressType
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)


from .forms import MacAddressTypeForm


class MacAddressTypeListView(LoginRequiredMixin, ListView):
    model = MacAddressType
    fields = "__All__"

    def get_queryset(self, *args, **kwargs):
        query = self.request.GET.get("q")
        if query:
            loockups = (
                Q(code__icontains=query)
                | Q(name__icontains=query)
                | Q(desc__icontains=query)
            )
            qs = MacAddressType.objects.filter(loockups)
        else:
            qs = super(MacAddressTypeListView, self).get_queryset(*args, **kwargs)

        return qs.order_by("-id")


class MacAddressTypeCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = MacAddressType
    form_class = MacAddressTypeForm
    success_message = 'MacAddressType "%(name)s" was created successfully'

    def get_initial(self):
        initial = super(MacAddressTypeCreateView, self).get_initial()
        initial["created_by"] = self.request.user
        initial["updated_by"] = self.request.user
        return initial

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.updated_by = self.request.user
        obj.save()
        return super(MacAddressTypeCreateView, self).form_valid(form)


class MacAddressTypeUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = MacAddressType
    success_message = 'MacAddressType "%(name)s" was updated successfully'

    form_class = MacAddressTypeForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.updated_by = self.request.user
        obj.save()
        return super(MacAddressTypeUpdateView, self).form_valid(form)


class MacAddressTypeDetailViev(LoginRequiredMixin, DetailView):
    model = MacAddressType
    fields = "__all__"


class MacAddressTypeDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = MacAddressType
    success_url = reverse_lazy("mac_address_types:list")
    success_message = 'MacAddressType "%(name)s" was deleted successfully'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = reverse_lazy("mac_address_types:list")
            return HttpResponseRedirect(url)
        else:
            return super(MacAddressTypeDeleteView, self).post(request, *args, **kwargs)

    def form_valid(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(MacAddressTypeDeleteView, self).delete(request, *args, **kwargs)
