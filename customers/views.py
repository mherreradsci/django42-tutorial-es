from django.http import HttpResponse

from .models import Customer


def index(request):
    customer_list = Customer.objects.all().order_by('-code')
    HTML = '<h1>Customers List</h1>'
    for customer_obj in customer_list:
        HTML += f'<li>{customer_obj.code} - {customer_obj.name}</li>'
    print(HTML)
    return HttpResponse(HTML)
