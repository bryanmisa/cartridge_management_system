from django.urls import path,include
from django.contrib.auth.views import LoginView
from item.views import *
from item.forms import UserLoginForm
from . import views

urlpatterns = [

    # Login / Logout URLS
    path(
        'login/',
        LoginView.as_view(
            template_name="login.html",
            authentication_form=UserLoginForm
            ),
        name='login'),

    # Hompage urls
    path('', views.dashboard, name='dashboard'),

    # Select2 URLS
    path("select2/", include("django_select2.urls")),

    # Printer URLS
    path('printer/list/', views.printer_list, name='printer_list'),
    path('printer/details/<int:id>', views.printer_details, name='printer_details'),
    path('printer/create', views.printer_create, name='printer_create'),
    path('printer/update/<int:id>', views.printer_update, name='printer_update'),
    path('printer/delete/<int:pk>', PrinterDeleteView.as_view(), name='delete_printer'),

    
    # Cartridge URLS
    path('cartridge/list/instock', views.cartridge_list_instock, name='cartridge_list_instock'),
    path('cartridge/list/installed', views.cartridge_list_installed, name='cartridge_list_installed'),
    path('cartridge/list/stocks/outofstock', views.list_of_out_of_stock_cartridges, name='list_of_out_of_stock_cartridges'),
    path('cartridge/update/<int:id>', views.cartridge_update, name='cartridge_update'),
    path('cartridge/dispose/<str:id>', views.dispose_cartridge, name='dispose_cartridge'),
    path('cartridge/create', views.cartridge_create, name='cartridge_create'),
    path('cartridge/install/<str:id>', views.install_cartridge, name='install_cartridge'),
    path('cartridge/copy/<str:id>', views.copy_cartridge, name='copy_cartridge'),
    path('catridge/details/<int:pk>', CartridgeDetailView.as_view(), name='cartridge_details'),


    # Location URLS
    path('item_location/list', views.location_list_view, name='list_location'),
    path('item_location/create', LocationCreateView.as_view(), name='create_location'),
    path('item_location/update/<int:pk>', LocationUpdateView.as_view(), name='update_location'),
    path('item_location/delete/<int:pk>', LocationDeleteView.as_view(), name='delete_location'),

    # Location URLS
    path('make/list', views.make_list_view, name='list_make'),
    path('make/create', MakeCreateView.as_view(), name='create_make'),
    path('make/update/<int:pk>', MakeUpdateView.as_view(), name='update_make'),
    path('make/delete/<int:pk>', MakeDeleteView.as_view(), name='delete_make'),

    # Cartridge Product No. URLS
    path('cartridge_product_no/list', views.cartridge_product_number_list_view, name='list_cartridge_product_no'),
    path('cartridge_product_no/create', CartridgeProductNumberCreateView.as_view(), name='create_cartridge_product_no'),
    path('cartridge_product_no/update/<int:pk>', CartridgeProductNumberUpdateView.as_view(), name='update_cartridge_product_no'),
    path('cartridge_product_no/delete/<int:pk>', CartProdDeleteView.as_view(), name='delete_cartridge_product_no'),

    # Printer Model URLS
    path('printer_model/list', views.printer_model_list_view, name='list_printer_model'),
    path('printer_model/create', PrinterModelCreateView.as_view(), name='create_printer_model'),
    path('printer_model/update/<int:pk>', PrinterModelUpdateView.as_view(), name='update_printer_model'),
    path('printer_model/delete/<int:pk>', PrinterModelDeleteView.as_view(), name='delete_printer_model'),

    # Vendor URLS
    path('vendor/list',views.vendor_list_view, name='list_vendor'),
    path('vendor/create', VendorCreateView.as_view(), name='create_vendor'),
    path('vendor/update/<int:pk>', VendorUpdateView.as_view(), name='update_vendor'),
    path('vendor/delete/<int:pk>', VendorDeleteView.as_view(), name='delete_vendor'),
    path('vendor/details/<int:pk>', VendorDetailView.as_view(), name='detail_vendor'),
]
