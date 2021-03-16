from django.contrib import admin
from .models import UserLogin, UserLogout

class UserLoginDisplay(admin.ModelAdmin):
	model = UserLogin
	list_display = ('username', 'date', 'time', 'success')

class UserLogoutDisplay(admin.ModelAdmin):
	model = UserLogout
	list_display = ('username', 'date', 'time')

admin.site.register(UserLogin, UserLoginDisplay)
admin.site.register(UserLogout, UserLogoutDisplay)
