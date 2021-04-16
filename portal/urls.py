from django.urls import path
from . import views

# list of URL's for this app
urlpatterns = [
    path('', views.portal_home, name="portal_home"),
    path('login-routing/', views.home, name='home'),
	path('register/', views.register, name='register-user'),
	path('driver_home/', views.driver_home, name='driver-home'),
    path('sponsor_home/', views.sponsor_home, name='sponsor-home'),
    path('admin/', views.GenericAdmin, name='admin-home'),
    path('catalog_sponsor/',views.catalog_sponsor, name='catalog-sponsor'),
    path('driver_catlogs/',views.driver_catalogs, name='driver-catalogs'),
    path('list_item/',views.sponsor_list, name='sponsor-list-item'),
    path('select_driver/',views.select_driver, name='select-driver'),
    path('cart/', views.Cart , name='Cart'),
    path('cart/<int:page_number>', views.Cart , name='Cart'),
    path('Order_history/<int:page_number>', views.Order_History , name='Order-History'),
    path('Order_history/', views.Order_History , name='Order-History'),
    path('Order_Placed/', views.Order_Placed , name='Order-Placed'),
    path('driver_product_home/', views.productListView, name='driver-product-home'),
    path('driver_product_home/<int:products_per_page>&<int:page_number>&<str:sponsor_company>', views.productListView, name='driver-product-home'),
    path('driver_product_home/', views.productDetailView, name="product-detail"),
    path('driver_product_home/<int:product_ID>&<str:sponsor_company>/', views.productDetailView, name="product-detail"),
]
