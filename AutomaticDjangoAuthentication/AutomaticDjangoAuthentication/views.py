from django.http import HttpResponse
from django.shortcuts import render

def home_view(request, *args, **kwargs):
    return HttpResponse("<h1>My Custom View</h1>")