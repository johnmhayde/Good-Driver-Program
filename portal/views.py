from django.shortcuts import render
from django.http import HttpResponse

# homepage view
def home(request):
	return HttpResponse('<h1>Portal Home</h1>')


# about page view
def about(request):
	return HttpResponse('<h1>Portal About</h1>')
