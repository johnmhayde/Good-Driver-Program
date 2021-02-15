from django.urls import path
from . import views

# list of URL's for this app
urlpatterns = [
    path('', views.portal_home, name='portal-home'),
	path('register/', views.register, name='register-user'),
	path('driver_home/', views.driver_home, name='driver-home'),
    path('sponsor_home/', views.sponsor_home, name='sponsor-home')
]
