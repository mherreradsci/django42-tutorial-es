from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from .forms import CustomerForm
from django.http import HttpResponse
from django.http import Http404
from django.urls import reverse, reverse_lazy

from .models import Customer
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)


def index(request):
    customer_list = Customer.objects.all().order_by("-code")
    HTML = "<h1>Customers - List</h1>"
    for customer_obj in customer_list:
        HTML += f"<li>{customer_obj.code} - {customer_obj.name}</li>"
    print(HTML)
    return HttpResponse(HTML)


def customer_list(request):
    context = {}
    context["object_list"] = Customer.objects.all()
    return render(request, "customers/customer_list.html", context)


class CustomerListView(ListView):
    model = Customer

    def get_queryset(self, *args, **kwargs):
        qs = super(CustomerListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs


def customer_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("customers:customer-list")
    else:
        form = CustomerForm()
    context = {"form": form}
    return render(request, "customers/customer_create.html", context)


class CustomerCreateView(CreateView):
    model = Customer
    fields = "__all__"
    template_name_suffix = "_create"


def customer_update(request, pk):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Customer, pk=pk)

    # pass the object as instance in form
    form = CustomerForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/customers/" + str(pk))

    # add form dictionary to context
    context["form"] = form

    return render(request, "customers/customer_update.html", context)


class CustomerUpdateView(UpdateView):
    model = Customer
    fields = "__all__"
    template_name_suffix = "_update"


def customer_detail0(request, pk):
    # dictionary for initial data with
    # field names as keys
    context = {}
    # add the dictionary during initialization
    context["data"] = Customer.objects.get(pk=pk)

    return render(request, "customers/customer_detail.html", context)


def customer_detail1(request, pk):
    # dictionary for initial data with
    # field names as keys
    try:
        customer_obj = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        raise Http404(f"Customer id:[{pk}] no existe")
    return render(
        request, "customers/customer_detail.html", context={"data": customer_obj}
    )


def customer_detail(request, pk):
    customer_obj = get_object_or_404(Customer, pk=pk)
    return render(
        request, "customers/customer_detail.html", context={"data": customer_obj}
    )


class CustomerDetailViev(DetailView):
    model = Customer
    fields = "__all__"


def customer_delete(request, pk):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Customer, pk=pk)

    if request.method == "POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        url = reverse("customers:list")
        return HttpResponseRedirect(url)

    return render(request, "customers/customer_delete.html", context)


class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy("customers:customer-list")
