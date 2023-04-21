from django.http import HttpResponse

from .models import Customer


def index(request):
    customer_obj = Customer.objects.get(id=2)

    HTML = f'<h1>Customer code: {customer_obj.code}</h1>'
    HTML += f'<li>Customer name: {customer_obj.name}</li>'
    print(HTML)
    return HttpResponse(HTML)
