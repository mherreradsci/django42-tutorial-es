from django.http import HttpResponse

from .models import Customer


def index(request):
    customer_list = Customer.objects.all().order_by('-code')
    HTML = '<h1>Customers List</h1>'
    for customer_obj in customer_list:
        HTML += f'<li>{customer_obj.code} - {customer_obj.name}</li>'
    print(HTML)
    return HttpResponse(HTML)


from .forms import CustomerForm
from django.shortcuts import redirect, render
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers:index')
    else:
        form = CustomerForm()
    context = {'form': form}
    return render(request, 'customers/customer_create.html', context)