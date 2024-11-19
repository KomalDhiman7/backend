from django.http import HttpResponse
from django.shortcuts import render

def home(request):
#   return HttpResponse("Hello World, you are at HOME page")
    return render (request, 'index.htm')

def about(request):
    return HttpResponse("Hello World, you are at ABOUT page")

def contact(request):
    return HttpResponse("Hello World, you are at CONTACT page")
