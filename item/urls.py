from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from item.views import *


urlpatterns = [

    # Login / Logout URLS


    # Hompage urls
    path('', views.dashboard, name='dashboard'),

    # Select2 URLS
    path("select2/", include("django_select2.urls")),

    # Printer URLS
    path('printer/list/instock/', views.printer_list_instock, name='printer_list_instock'),
    path('printer/list/deployed', views.printer_list_deployed, name='printer_list_deployed'),
    path('printer/details/<int:id>', views.printer_details, name='printer_details'),
    path('printer/create', views.printer_create, name='printer_create'),
    path('printer/update/<int:id>', views.printer_update, name='printer_update'),
    path('printer/deploy/<int:id>', views.deploy_printer, name='deploy_printer'),
    
    # Cartridge URLS
    path('cartridge/list/instock', views.cartridge_list_instock, name='cartridge_list_instock'),
    path('cartridge/list/installed', views.cartridge_list_installed, name='cartridge_list_installed'),
    path('cartridge/list/stocks', views.list_cartridge_stocks, name='list_cartridge_stocks'),
    path('cartridge/update/<int:id>', views.cartridge_update, name='cartridge_update'),
    path('cartridge/create', views.cartridge_create, name='cartridge_create'),
    path('cartridge/install/<str:id>', views.install_cartridge, name='install_cartridge'),

    # Location URLS
    path('item_location/list', LocationListView.as_view(), name='list_location'),
    path('item_location/create', LocationCreateView.as_view(), name='create_location'),
    path('item_location/update/<int:pk>', LocationUpdateView.as_view(), name='update_location'),
    path('item_location/delete/<int:pk>', LocationDeleteView.as_view(), name='delete_location'),

    # Location URLS
    path('make/list', MakeListView.as_view(), name='list_make'),
    path('make/create', MakeCreateView.as_view(), name='create_make'),
    path('make/update/<int:pk>', MakeUpdateView.as_view(), name='update_make'),
    path('make/delete/<int:pk>', MakeDeleteView.as_view(), name='delete_make'),

    # Cartridge Product No. URLS
    path('cartridge_product_no/list', CartridgeProductNumberListView.as_view(), name='list_cartridge_product_no'),
    path('cartridge_product_no/create', CartridgeProductNumberCreateView.as_view(), name='create_cartridge_product_no'),
    path('cartridge_product_no/update/<int:pk>', CartridgeProductNumberUpdateView.as_view(), name='update_cartridge_product_no'),
    path('cartridge_product_no/delete/<int:pk>', CartProdDeleteView.as_view(), name='delete_cartridge_product_no'),

    # Printer Model URLS
    path('printer_model/list', PrinterModelListView.as_view(), name='list_printer_model'),
    path('printer_model/create', PrinterModelCreateView.as_view(), name='create_printer_model'),
    path('printer_model/update/<int:pk>', PrinterModelUpdateView.as_view(), name='update_printer_model'),
    path('printer_model/delete/<int:pk>', PrinterModelDeleteView.as_view(), name='delete_printer_model'),
]
