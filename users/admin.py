from django.contrib import admin
from .models import Driver

class AdminDriver(admin.ModelAdmin):
	model = Driver
	list_display = ('username', 'password', 'first_name', 'last_name', 'phone_num', 'email', 'address')

admin.site.register(Driver, AdminDriver)
