from django.shortcuts import render
from django.http import HttpResponse

# send user to homepage
def home(request):
	return render(request, 'portal/home.html')

def register(request):
	return render(request, 'portal/register.html')
