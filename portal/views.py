from django.shortcuts import render
from django.http import HttpResponse

# send user to homepage
def home(request):
	return render(request, 'portal/home.html')
