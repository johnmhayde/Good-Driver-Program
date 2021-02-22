from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
	path('register/', user_views.register, name="driver_register"),
    path('sponsor_register/', user_views.register_sponsor, name="sponsor_register"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
	path('', include('portal.urls')),
    path('edit_info/', user_views.update_driver_info, name="update-info")
]
