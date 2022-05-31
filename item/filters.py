from django_filters import *
from item.widgets import *
from item.models import *
import django_filters

class CartridgeProductNumberFilter(django_filters.FilterSet):
    
    name = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta :
        model = CartridgeProductNumber
        fields = ['name','color', 'cartridge_type' ]

class CartridgeFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains')
    printer = django_filters.CharFilter(lookup_expr='icontains',field_name='printer__name',label='Printer')
    printer_model = django_filters.CharFilter(lookup_expr='icontains',field_name='printer_model__name',label='Printer Model')
    make = django_filters.CharFilter(lookup_expr='icontains',field_name='make__name',label='Make')
    cart_prod_no = django_filters.CharFilter(lookup_expr='icontains',field_name='cart_prod_no__name',label='Cartridge Product Number')
    start_date = DateFilter(field_name ='installed_date',lookup_expr=('gt'),widget=DatePickerInput({'type': 'date'})) 
    end_date = DateFilter(field_name='installed_date',lookup_expr=('lt'),widget=DatePickerInput({'type': 'date'}))
    date_range = DateRangeFilter(field_name='installed_date',widget=DatePickerInput({'type': 'date'}))

    class Meta :
        model = Cartridge
        fields = ['name', 'status' ,'printer', 'printer_model', 'cart_prod_no', 'make',]

class PrinterFilter(django_filters.FilterSet):

    name = django_filters.CharFilter(lookup_expr='icontains',label='Name')
    make = django_filters.CharFilter(lookup_expr='icontains',field_name='make__name',label='Make')
    printer_model = django_filters.CharFilter(lookup_expr='icontains',field_name='printer_model__name',label='Printer Model')
    asset_tag = django_filters.CharFilter(lookup_expr='icontains',field_name='asset_tag__name',label='Asset')
    location = django_filters.CharFilter(lookup_expr='icontains',field_name='location__name',label='Location')
    start_date = DateFilter(field_name ='installed_date',lookup_expr=('gt'),widget=DatePickerInput({'type': 'date'})) 
    end_date = DateFilter(field_name='installed_date',lookup_expr=('lt'),widget=DatePickerInput({'type': 'date'}))
    date_range = DateRangeFilter(field_name='installed_date',widget=DatePickerInput({'type': 'date'}))

    class Meta :
        model = Printer
        fields = ['name', 'make', 'printer_model', 'asset_tag', 'location']

class PrinterModelFilter(django_filters.FilterSet):
     name = django_filters.CharFilter(lookup_expr='icontains',label='Name')
     model = Make
     fields = ['name']

class LocationFilter(django_filters.FilterSet):
     name = django_filters.CharFilter(lookup_expr='icontains',label='Name')
     model = Location
     fields = ['name']

class MakeFilter(django_filters.FilterSet):
     name = django_filters.CharFilter(lookup_expr='icontains',label='Name')
     model = Make
     fields = ['name']

class VendorFilter(django_filters.FilterSet):
     name = django_filters.CharFilter(lookup_expr='icontains',label='Name')
     model = Vendor
     fields = ['company_name']

