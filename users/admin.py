from django.contrib import admin
from .models import Driver, GenericUser

class AdminDriver(admin.ModelAdmin):
	model = Driver
	list_display = ('username', 'password', 'first_name', 'last_name', 'phone_num', 'email', 'address')

class AdminGenericUser(admin.ModelAdmin):
	model = GenericUser
	list_display = ('username', 'password', 'type')

admin.site.register(Driver, AdminDriver)
admin.site.register(GenericUser, AdminGenericUser)
