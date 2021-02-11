from django.contrib import admin
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
	path('register/', user_views.register, name="driver_register"),
    path('sponsor_register/', user_views.register_sponsor, name="sponsor_register"),
	path('', include('portal.urls')),
]
