from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
	path('register/', user_views.register, name="driver_register"),
    path('sponsor_register/', user_views.register_sponsor, name="sponsor_register"),
    path('add_a_sponsor/', user_views.register_sponsor_P2P, name="sponsor_register_p2p"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
	path('', include('portal.urls')),
    path('edit_info/', user_views.update_driver_info, name="update-info"),
    path('edit_sponsor_info/', user_views.update_sponsor_info, name="update-sponsor-info"),
    path('application/', user_views.application, name="apply"),
    path('password_reset', user_views.password_reset_request, name='password_reset'),
    path('password_reset_done/<userType>/<username>', user_views.password_change_request, name='password_reset_done'),
    path('reset/<username>/', user_views.password_update_request, name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='change-password.html', success_url = '/'), name='change_password'),
    path('edit_points/', user_views.update_driver_points, name="update-points"),
    path('edit_points_rate/', user_views.update_driver_points_rate, name="update-points-rate"),
    path('accept_application', user_views.accept_application, name="accept-application"),
    path('generate_driver_points_report/', user_views.generate_driver_points_report, name='generate-driver-points')
]

# urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Good Driver Program Administration'
