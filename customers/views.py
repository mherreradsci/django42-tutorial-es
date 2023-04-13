from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    # dir returns list of the attributes and methods of 
    # any object (say functions , modules, strings, lists, dictionaries etc.)
    print('>>>>>', dir(request)) 
    return HttpResponse("Hello, world. You're at the customers index.")

