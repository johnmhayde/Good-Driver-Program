from django.shortcuts import render
from django.http import HttpResponse
from users.models import Driver
from django.contrib.auth.models import User

# send user to homepage
def home(request):
	return render(request, 'portal/home.html')

def register(request):
	return render(request, 'portal/register.html')

def driver_home(request):
	# send driver info to page
	user = request.user
	driver = Driver.objects.get(username=user.username)
	data = {
	"points" : driver.points
	}
	return render(request, 'portal/driver_home.html', data)

def sponsor_home(request):
	return render(request, 'portal/home.html')
