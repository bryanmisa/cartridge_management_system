from itertools import count
from msilib.schema import ListView
from django import views
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import (View,
                                  ListView,
                                  DeleteView,
                                  UpdateView,
                                  CreateView,
                                  DetailView,)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from django.urls import reverse_lazy
from item.models import *
from item.forms import *
from item.filters import *

# Home Page View
@login_required
def dashboard(request):
    cartridges = CartridgeProductNumber.objects.annotate(number_of_cartridges = 
                                                        Count('cart_prod_no',
                                                        filter=Q(cart_prod_no__status='In Stock'),distinct=True)
                                                        ).order_by('updated_at')[:11]
    #Paginate List of Stocks, 
    page = request.GET.get('page', 1)
    paginator = Paginator(cartridges, 10)

    try:
        cartridges = paginator.page(page) 
    except PageNotAnInteger:
        cartridges = paginator.page(1)
    except EmptyPage:
        cartridges = paginator.page(paginator.num_pages)

    context = {
        'cartridges' : cartridges,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def list_of_out_of_stock_cartridges(request):

    cartridges = CartridgeProductNumber.objects.annotate(number_of_cartridges = 
                                                        Count('cart_prod_no',
                                                        filter=Q(cart_prod_no__status='In Stock'))).order_by('number_of_cartridges')
    cartridge_filter = CartridgeProductNumberFilter(request.GET, queryset = cartridges)
    cartridges = cartridge_filter.qs

    #Paginate List of Stocks, 

    page = request.GET.get('page', 1)
    paginator = Paginator(cartridges, 10)

    try:
        cartridges = paginator.page(page) 
    except PageNotAnInteger:
        cartridges = paginator.page(1)
    except EmptyPage:
        cartridges = paginator.page(paginator.num_pages)
    
    # returning the querysets
    context = {
        'cartridges' : cartridges,
        'cartridge_filter' : cartridge_filter,
    }
    return render(request, 'cartridge/cartridge_list_of_stock_cartridges.html', context)

#### Printer Model Views
@login_required
def printer_list(request):
    printers = Printer.objects.all()
    printer_filter = PrinterFilter(request.GET, queryset = printers)
    printers = printer_filter.qs

    page = request.GET.get('page', 1)
    paginator = Paginator(printers, 10)

    try:
        printers = paginator.page(page)
    except PageNotAnInteger:
        printers = paginator.page(1)
    except EmptyPage:
        printers = paginator.page(paginator.num_pages)

    context = {
        'printers' : printers,
        'printer_filter' : printer_filter,
    }
    return render(request, 'printer/printer_list.html', context)


@login_required
def printer_details(request, id):
    printer_detail = Printer.objects.get(id = id)
    cartridges = Cartridge.objects.filter(printer = printer_detail.id)
    context = {
        'printer_detail' : printer_detail,
        'cartridges' : cartridges,
    }
    return render(request, 'printer/printer_details.html', context)

@login_required
def printer_create(request):
    context = {}
    form = PrinterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('printer_list')
    context['form'] = form
    return render(request, 'printer/printer_form.html', context)

@login_required
def printer_update(request, id):
    printer = get_object_or_404(Printer, pk = id)
    form = PrinterForm(instance=printer)

    if request.method == "POST":
        form = PrinterForm(request.POST, instance=printer)
        if form.is_valid():
            form.save()
            return redirect('printer_list_deployed')
    context = {
        'form' : form,
    }

    return render(request, 'printer/printer_form.html', context)

class PrinterDeleteView(LoginRequiredMixin, DeleteView):
    model = Printer
    template_name = 'printer/delete_printer.html'
    success_url = reverse_lazy('printer_list')

# Printer Model Views

@login_required
def printer_model_list_view(request):
    printer_model_list = PrinterModel.objects.all()
    printer_model_filter = PrinterModelFilter(request.GET, queryset = printer_model_list)
    printer_model_list_qs = printer_model_filter.qs

    # Paginate Cartridge Product Number
    page = request.GET.get('page', 1)
    paginator = Paginator(printer_model_list_qs, 10) # Paginate by 10

    try:
        printer_model_list_qs = paginator.page(page) 
    except PageNotAnInteger:
        printer_model_list_qs = paginator.page(1)
    except EmptyPage:
        printer_model_list_qs = paginator.page(paginator.num_pages)
    
    # returning the querysets
    context = {
        'printer_model_list_qs' : printer_model_list_qs,
        'printer_model_filter' : printer_model_filter,
    }
    return render(request, 'printer/printer_model/list_printer_model.html', context)  

class PrinterModelUpdateView(LoginRequiredMixin, UpdateView):

    model = PrinterModel
    fields = '__all__'
    context_object_name = 'printer_model'
    template_name ='printer/printer_model/form_printer_model.html'
    success_url =  reverse_lazy('list_printer_model')

class PrinterModelDeleteView(LoginRequiredMixin, DeleteView):
    model = PrinterModel
    context_object_name = 'printer_model'
    template_name = 'printer/printer_model/delete_printer_model.html'
    success_url = reverse_lazy('list_printer_model')

class PrinterModelCreateView(LoginRequiredMixin, CreateView):
    model = PrinterModel
    fields = ('name',)
    context_object_name = 'printer_model'
    template_name = 'printer/printer_model/form_printer_model.html'
    success_url = reverse_lazy('list_printer_model')
 
# Item Cartridge Views
@login_required
def cartridge_list_instock(request):
    cartridges_list = Cartridge.objects.all().filter(status='In Stock')
    cartridge_filter = CartridgeInStockFilter(request.GET, queryset = cartridges_list)
    cartridges_qs = cartridge_filter.qs
    
    #Paginate Cartridges
    page = request.GET.get('page', 1)
    paginator = Paginator(cartridges_qs, 10)

    try:
        cartridges_qs = paginator.page(page) 
    except PageNotAnInteger:
        cartridges_qs = paginator.page(1)
    except EmptyPage:
        cartridges_qs = paginator.page(paginator.num_pages)
    
    # returning the querysets
    context = {
        'cartridges_qs' : cartridges_qs,
        'cartridge_filter' : cartridge_filter,
    }
    return render(request, 'cartridge/cartridge_instock_list.html', context)

@login_required
def cartridge_list_installed(request):
    cartridges = Cartridge.objects.all().filter(status='Installed')
    cartridge_filter = CartridgeInstalledFilter(request.GET, queryset = cartridges)
    cartridges = cartridge_filter.qs
    
    #Paginate Cartridges
    page = request.GET.get('page', 1)
    paginator = Paginator(cartridges, 10)

    try:
        cartridges = paginator.page(page) 
    except PageNotAnInteger:
        cartridges = paginator.page(1)
    except EmptyPage:
        cartridges = paginator.page(paginator.num_pages)
    
    # returning the querysets
    context = {
        'cartridges' : cartridges,
        'cartridge_filter' : cartridge_filter,
    }
    return render(request, 'cartridge/cartridge_installed_list.html', context)

@login_required
def cartridge_update(request, id):

    data = get_object_or_404(Cartridge, pk = id)
    form = CartridgeForm(instance=data)

    if request.method == "POST":
        form = CartridgeForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('cartridge_list_instock')

    context = {
        'form' : form,
    }

    return render(request, 'cartridge/cartridge_create_form.html', context) # render querysets on the HTML

@login_required
def dispose_cartridge(request, id):

    data = get_object_or_404(Cartridge, pk = id)
    form = DisposeCartridgeForm(instance=data)

    if request.method == "POST":
        form = DisposeCartridgeForm(request.POST, instance=data)
        if form.is_valid():
            data.status = 'Disposed'
            form.save()
            return redirect('cartridge_list_installed')
            
    context = {
        'form' : form,
    }

    return render(request, 'cartridge/cartridge_dispose_form.html', context)

@login_required
def install_cartridge(request, id):

    data = get_object_or_404(Cartridge, pk = id)
    form = InstallCartridgeForm(instance=data)

    if request.method == "POST":
        form = InstallCartridgeForm(request.POST, instance=data)
        if form.is_valid():
            data.status = 'Installed'
            #data.installed_date = date.today()
            form.save()
            return redirect('cartridge_list_installed')
            
    context = {
        'form' : form,
    }

    return render(request, 'cartridge/cartridge_install_form.html', context)

@login_required
def cartridge_create(request):
    context = {}
    form = CartridgeForm(request.POST or None)
   
    if request.method == "POST":

        if form.is_valid():
            form = form.save(commit=False)

            form.save()
            return redirect('cartridge_list_instock')
    context['form'] = form

    return render(request, 'cartridge/cartridge_create_form.html', context)

@login_required
def copy_cartridge(request, id):
    copy_cartridge= get_object_or_404(Cartridge, pk = id)
    copy_cartridge.pk=None
    copy_cartridge.save()
    return redirect('cartridge_list_instock')



class CartridgeDetailView(LoginRequiredMixin, DetailView):
    model = Cartridge
    fields = '__all__'
    context_object_name = 'cartridge'
    template_name = "cartridge/cartridge_details.html"
    success_url = reverse_lazy('cartridge_list_instock')


# Cartridge Product Number View

@login_required
def cartridge_product_number_list_view(request):
    cart_prod_list = CartridgeProductNumber.objects.all()
    cart_prod_list_filter = CartridgeProductNumberFilter(request.GET, queryset = cart_prod_list)
    cart_prod_list_qs = cart_prod_list_filter.qs

    # Paginate Cartridge Product Number
    page = request.GET.get('page', 1)
    paginator = Paginator(cart_prod_list_qs, 10)

    try:
        cart_prod_list_qs = paginator.page(page) 
    except PageNotAnInteger:
        cart_prod_list_qs = paginator.page(1)
    except EmptyPage:
        cart_prod_list_qs = paginator.page(paginator.num_pages)
    
    # returning the querysets
    context = {
        'cart_prod_list_qs' : cart_prod_list_qs,
        'cart_prod_list_filter' : cart_prod_list_filter,
    }
    return render(request, 'cartridge/cartridge_product_no/list_cartridge_product_no.html', context)    

class CartridgeProductNumberUpdateView(LoginRequiredMixin, UpdateView):
    model = CartridgeProductNumber
    fields = '__all__'
    template_name ='cartridge/cartridge_product_no/form_cartridge_product_no.html'
    success_url =  reverse_lazy('list_cartridge_product_no')

class CartProdDeleteView(LoginRequiredMixin, DeleteView):
    model = CartridgeProductNumber
    template_name = 'cartridge/cartridge_product_no/del_cartridge_product_no.html'
    success_url = reverse_lazy('list_cartridge_product_no')

class CartridgeProductNumberCreateView(LoginRequiredMixin, CreateView):
    model = CartridgeProductNumber
    fields = '__all__'
    template_name = 'cartridge/cartridge_product_no/form_cartridge_product_no.html'
    success_url = reverse_lazy('list_cartridge_product_no')

# Location Views

@login_required 
def location_list_view(request):
    location_list = Location.objects.all()
    location_list_filter = LocationFilter(request.GET, queryset = location_list)
    location_list_qs = location_list_filter.qs

    # Paginate Cartridge Product Number
    page = request.GET.get('page', 1)
    paginator = Paginator(location_list_qs, 10)

    try:
        location_list_qs = paginator.page(page) 
    except PageNotAnInteger:
        location_list_qs = paginator.page(1)
    except EmptyPage:
        location_list_qs = paginator.page(paginator.num_pages)
    
    # returning the querysets
    context = {
        'location_list_qs' : location_list_qs,
        'location_list_filter' : location_list_filter,
    }
    return render(request, 'item_location/list_location.html', context)   

class LocationUpdateView(LoginRequiredMixin, UpdateView):
    model = Location
    fields = '__all__'
    template_name ='item_location/form_location.html'
    success_url =  reverse_lazy('list_location')

class LocationDeleteView(LoginRequiredMixin, DeleteView):
    model = Location
    template_name = "item_location/delete_location.html"
    success_url = reverse_lazy('list_location')

class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    fields = ('name',)
    template_name = "item_location/form_location.html"
    success_url = reverse_lazy('list_location')

# Make Views

@login_required
def make_list_view(request):
    make_list = Make.objects.all()
    make_list_filter = MakeFilter(request.GET, queryset = make_list)
    make_list_qs = make_list_filter.qs

    # Paginate Cartridge Product Number
    page = request.GET.get('page', 1)
    paginator = Paginator(make_list_qs, 10)

    try:
        make_list_qs = paginator.page(page) 
    except PageNotAnInteger:
        make_list_qs = paginator.page(1)
    except EmptyPage:
        make_list_qs = paginator.page(paginator.num_pages)
    
    # returning the querysets
    context = {
        'make_list_qs' : make_list_qs,
        'make_list_filter' : make_list_filter,
    }
    return render(request, 'make/list_make.html', context)   

class MakeUpdateView(LoginRequiredMixin, UpdateView):
    model = Make
    fields = '__all__'
    template_name ='make/form_make.html'
    success_url =  reverse_lazy('list_make')

class MakeDeleteView(LoginRequiredMixin, DeleteView):
    model = Make
    template_name = "make/delete_make.html"
    success_url = reverse_lazy('list_make')

class MakeCreateView(LoginRequiredMixin, CreateView):
    model = Make
    fields = ('name',)
    template_name = "make/form_make.html"
    success_url = reverse_lazy('list_make')

@login_required
def vendor_list_view(request) :
    vendor_list = Vendor.objects.all()
    vendor_list_filter = VendorFilter(request.GET, queryset = vendor_list)
    vendor_list_qs = vendor_list_filter.qs

    # Paginate Cartridge Product Number
    page = request.GET.get('page', 1)
    paginator = Paginator(vendor_list_qs, 10)

    try:
        vendor_list_qs = paginator.page(page) 
    except PageNotAnInteger:
        vendor_list_qs = paginator.page(1)
    except EmptyPage:
        vendor_list_qs = paginator.page(paginator.num_pages)
    
    # returning the querysets
    context = {
        'vendor_list_qs' : vendor_list_qs,
        'vendor_list_filter' : vendor_list_filter,
    }
    return render(request, 'vendor/list_vendor.html', context)   

class VendorUpdateView(LoginRequiredMixin, UpdateView):
    model = Vendor
    fields = '__all__'
    template_name ='vendor/form_vendor.html'
    success_url =  reverse_lazy('list_vendor')

class VendorDeleteView(LoginRequiredMixin, DeleteView):
    model = Vendor
    template_name = "vendor/delete_vendor.html"
    success_url = reverse_lazy('list_vendor')

class VendorCreateView(LoginRequiredMixin, CreateView):
    model = Vendor
    fields = '__all__'
    template_name = "vendor/form_vendor.html"
    success_url = reverse_lazy('list_vendor')

class VendorDetailView(LoginRequiredMixin, DetailView):
    model = Vendor
    fields = '__all__'
    context_object_name = 'vendor'
    template_name = "vendor/details_vendor.html"
    success_url = reverse_lazy('list_vendor')