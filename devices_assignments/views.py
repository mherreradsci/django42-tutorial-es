from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView

from customers.models import Customer
from devices_assignments.forms import CustomerForm, DeviCustAssignmentFormset


class CustomerUpdateView(
    SuccessMessageMixin, LoginRequiredMixin, UpdateView  # CustomerInline,
):
    form_class = CustomerForm
    model = Customer
    template_name = "devices_assignments/assignments_update.html"

    success_message = 'Customer "%(name)s" was updated successfully'
    success_message_inline_upd = 'Device "%(name)s" was updated successfully'
    success_message_inline_del = 'Device "%(name)s" was deleted successfully'

    def get_context_data(self, **kwargs):
        context = super(CustomerUpdateView, self).get_context_data(**kwargs)
        context["named_formsets"] = self.get_named_formsets()
        return context

    def get_named_formsets(self):
        return {
            "assignments": DeviCustAssignmentFormset(
                self.request.POST or None,
                self.request.FILES or None,
                instance=self.object,
                prefix="assignments",
            ),
            # "images": ImageFormSet(
            #     self.request.POST or None,
            #     self.request.FILES or None,
            #     instance=self.object,
            #     prefix="images",
            # ),
        }

    def get_success_url(
        self,
    ):
        messages.add_message(
            self.request,
            messages.INFO,
            self.success_message % {"name": self.object},
        )
        if self.request.POST.get("_continue"):
            success_url = reverse(
                "devices_assignments:update", kwargs={"pk": self.object.pk}
            )
        elif self.request.POST.get("_save"):
            success_url = reverse("devices:list")
        else:
            success_url = None
        return success_url

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()

        # if not all((x.is_valid() for x in named_formsets.values())):
        #     return self.render_to_response(self.get_context_data(form=form))

        all_valid = True
        for fs in named_formsets.values():
            if not fs.is_valid():
                all_valid = False

        if not all_valid:
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

        return redirect(self.get_success_url())

    def formset_assignments_valid(self, formset):
        """
        Hook for custom formset saving. Useful if you have multiple formsets
        """
        assignments = formset.save(commit=False)
        # add this, if you have can_delete=True parameter set in
        # inlineformset_factory func

        for obj in formset.deleted_objects:
            del_name = obj
            obj.delete()
            messages.add_message(
                self.request,
                messages.INFO,
                self.success_message_inline_del % {"name": del_name},
            )

        for assignment in assignments:
            if assignment.id:
                assignment.updated_by = self.request.user
            else:
                assignment.created_by = self.request.user
                assignment.updated_by = self.request.user
            messages.add_message(
                self.request,
                messages.INFO,
                self.success_message_inline_upd % {"name": assignment.device},
            )
            assignment.customer = self.object
            assignment.save()

    def get_initial(self):
        initial = super(CustomerUpdateView, self).get_initial()
        initial["created_by"] = self.request.user
        initial["updated_by"] = self.request.user
        return initial
