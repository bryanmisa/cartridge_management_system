from django import forms
from item.models import *
from .widgets import DatePickerInput
from django_select2 import forms as s2forms
from django.contrib.auth.forms import AuthenticationForm,UsernameField



# Widgets for Select2
class PrinterWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        'name__icontains'
    ]

class PrinterModelWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        'name__icontains'
    ]

class CartridgeProductNoWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        'name__icontains'
    ]

class MakeWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        'name__icontains'
    ]

class LocationWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        'name__icontains'
    ]

class VendorWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        'company_name__icontains'
    ]

# Forms
class PrinterForm(forms.ModelForm):

    class Meta:

        model = Printer
        fields = ['name', 'asset_tag', 'serial_number', 'owned_by', 'location', 'printer_model', 'make', 'vendor']
        labels = {
            'name': 'Printer',
            'asset_tag' : 'Asset Tag',  
            'serial_number' : 'Serial Number', 
            'location' : 'Located at', 
            'printer_model' : 'Printer Model', 
            'make' : 'Make',
            'vendor' : 'Vendor',
        }
        
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'status' : forms.Select(attrs={'class':'form-control'}),
            'asset_tag' : forms.TextInput(attrs={'class':'form-control'}),
            'serial_number' : forms.TextInput(attrs={'class':'form-control'}),
            'owned_by' : forms.Select(attrs={'class':'form-control'}),
            'location' : LocationWidget(attrs={'class':'form-control'}),
            'printer_model' : PrinterModelWidget(attrs={'class':'form-control'}),
            'make': MakeWidget(attrs={'class':'form-control',}),
            'vendor' : VendorWidget(attrs={'class':'form-control',}),
        }
        
class DeployPrinterForm(forms.ModelForm):
    class Meta:
        model = Printer
        fields = ['location', 'installed_date']
        labels = {
                'location' : 'Set the Location of the Printer',
                'installed_date' : 'Deployed Date'
            }
        widgets = {
            'location' : LocationWidget(attrs={'class':'form-control'}),
            'installed_date' : DatePickerInput(attrs={'class':'form-control'}),
        }

class CartridgeForm(forms.ModelForm):
    
    class Meta:

        model = Cartridge
        fields = ['name', 'printer_model' ,'cart_prod_no', 'make', 'vendor']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'printer_model' : PrinterModelWidget(attrs={'class':'form-control'}),
            'cart_prod_no' : CartridgeProductNoWidget(attrs={'class':'form-control'}),
            'make' : MakeWidget(attrs={'class':'form-control'}),
            'vendor' : VendorWidget(attrs={'class':'form-control',}),
        }
        
class InstallCartridgeForm(forms.ModelForm):
    
    class Meta:

        model = Cartridge
        fields = ['printer','installed_date']

        widgets = {
            'printer' : PrinterWidget(attrs={'class':'form-control'}),
            'installed_date' : DatePickerInput(attrs={'class':'form-control'}),
        }

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'hi',
        }))