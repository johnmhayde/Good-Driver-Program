from django.urls import path
from . import views

# list of URL's for this app
urlpatterns = [
    path('', views.home, name='portal-home'),
	path('register/', views.register, name='register-user')
]
