from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from .models import Device
from django.views.generic import (
    ListView,
    # CreateView,
    # UpdateView,
    DetailView,
    DeleteView,
    FormView,
)

from django.views.generic.edit import CreateView, UpdateView

from django.views.generic.detail import SingleObjectMixin
from .forms import DeviceForm, DeviceMacAddressFormset
from mac_addresses.models import MacAddress


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

    def get_template_names(self):
        if self.request.htmx and not self.request.htmx.history_restore_request:
            return "devices/partials/device_table.html"
        return "devices/device_list.html"


class DeviceInline:
    form_class = DeviceForm
    model = Device
    template_name = "devices/device_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()

        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        obj = form.save(commit=False)
        if obj.id:
            obj.updated_by = self.request.user
        else:
            obj.created_by = self.request.user
            obj.updated_by = self.request.user

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, "formset_{0}_valid".format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect("devices:list")

    def formset_macaddress_formset_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        macaddresses = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for macaddress in macaddresses:
            if macaddress.id:
                macaddress.updated_by = self.request.user
            else:
                macaddress.created_by = self.request.user
                macaddress.updated_by = self.request.user

            macaddress.device = self.object
            macaddress.save()


class DeviceCreateView(
    SuccessMessageMixin, LoginRequiredMixin, DeviceInline, CreateView
):
    success_message = 'Device "%(name)s" was created successfully'

    def get_context_data(self, **kwargs):
        context = super(DeviceCreateView, self).get_context_data(**kwargs)
        context["named_formsets"] = self.get_named_formsets()

        return context

    def get_initial(self):
        initial = super(DeviceCreateView, self).get_initial()
        initial["created_by"] = self.request.user
        initial["updated_by"] = self.request.user
        return initial

    def get_named_formsets(self):
        if self.request.method == "POST":
            return {
                "macaddress_formset": DeviceMacAddressFormset(
                    self.request.POST or None,
                    self.request.FILES or None,
                    prefix="macaddress_formset",
                ),
                # 'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
            }

        else:
            return {
                "macaddress_formset": DeviceMacAddressFormset(
                    prefix="macaddress_formset"
                ),
                # 'images': ImageFormSet(prefix='images'),
            }


class DeviceUpdateView(
    SuccessMessageMixin, LoginRequiredMixin, DeviceInline, UpdateView
):
    success_message = 'Device "%(name)s" was updated successfully'

    def get_context_data(self, **kwargs):
        context = super(DeviceUpdateView, self).get_context_data(**kwargs)
        context["named_formsets"] = self.get_named_formsets()
        return context

    def get_named_formsets(self):
        return {
            "macaddress_formset": DeviceMacAddressFormset(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.object,
                prefix="macaddress_formset",
            ),
            # 'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='images'),
        }


def delete_macaddress(request, pk):
    try:
        macaddress = MacAddress.objects.get(id=pk)
    except MacAddress.DoesNotExist:
        messages.success(request, "Object Does not exit")
        return redirect("devices:update_device", pk=macaddress.device.id)

    macaddress.delete()
    messages.success(request, "MacAddress deleted successfully")
    return redirect("devices:update_device", pk=macaddress.device.id)


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
