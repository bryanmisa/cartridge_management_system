from itertools import count
from msilib.schema import ListView
from django import views
from django.shortcuts import render, redirect, get_object_or_404
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


# Create your views here.


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
    
    return render(request, 'index.html', context)

@login_required
def list_of_out_of_stock_cartridges(request):

    cartridges = CartridgeProductNumber.objects.annotate(number_of_cartridges = 
                                                        Count('cart_prod_no',
                                                        filter=Q(cart_prod_no__status='In Stock')))
                                                        
    cartridge_filter = CartridgeProductNumberFilter(request.GET, queryset = cartridges)
    cartridges = cartridge_filter.qs.order_by('name')

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
    return render(request, 'cartridge/cartridge_list_of_out_of_stocks.html', context)

#### Printer Model Views
@login_required
def printer_list_instock(request):
    printers = Printer.objects.all().filter(status='In Stock')
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
def printer_list_deployed(request):
    printers = Printer.objects.all().filter(status='Deployed')
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
            return redirect('printer_list_instock')
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

@login_required
def deploy_printer(request, id):

    data = get_object_or_404(Printer, pk = id)
    form = DeployPrinterForm(instance=data)

    if request.method == "POST":
        form = DeployPrinterForm(request.POST, instance=data)
        if form.is_valid():
            data.status = 'Deployed'
            form.save()
            return redirect('printer_list_deployed')
            
    context = {
        'form' : form,
    }

    return render(request, 'printer/printer_form.html', context)

# Printer Model Views

class PrinterModelListView(LoginRequiredMixin, ListView):
    model = PrinterModel
    template_name = 'printer/printer_model/list_printer_model.html'
    context_object_name = 'printer_models'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = PrinterModelFilter(self.request.GET, queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = PrinterModelFilter(self.request.GET, queryset)
        context["printer_models"] = filter
        return context

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
 
# ITEM CARTRIDGE VIEWS
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



# class CartridgeListInStockView(LoginRequiredMixin, ListView):
#     model = Cartridge
#     context_object_name = 'cartridges'
#     template_name = 'cartridge/cartridge_instock_list.html' 
#     paginate_by = 10

#     def get_queryset(self):
#         queryset = super().get_queryset()
        
#         filter = CartridgeInStockFilter(self.request.GET, queryset)
#         return filter.qs

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         queryset = self.get_queryset()
#         filter = CartridgeInStockFilter(self.request.GET, queryset)
#         context["cartridges"] = filter
#         return context


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
            return redirect('cartridge_list_installed')

    context = {
        'form' : form,
    }

    return render(request, 'cartridge/cartridge_create_form.html', context) # render querysets on the HTML

# @login_required
# def cartridge_create(request):
#     context = {}
#     form = CartridgeForm(request.POST or None)
#     number_of_cartridges = request.POST.get('count_of_cartridges')
#     if request.method == "POST":
#         if form.is_valid():
#             cartridges = form.save()
            
#             return redirect('cartridge_list_instock')
    
#     context['form'] = form

#     return render(request, 'cartridge/cartridge_create_form.html', context)

class CartridgeCreateView(LoginRequiredMixin, CreateView):
    model = Cartridge
    form_class = CartridgeForm
    template_name = 'cartridge/cartridge_create_form.html'
    success_url = reverse_lazy('cartridge_list_instock')

@login_required
def copy_cartridge(request, id):
    copy_cartridge= get_object_or_404(Cartridge, pk = id)
    copy_cartridge.pk=None
    copy_cartridge.save()
    return redirect('cartridge_list_instock')

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

class CartridgeDetailView(LoginRequiredMixin, DetailView):
    model = Cartridge
    fields = '__all__'
    context_object_name = 'cartridge'
    template_name = "cartridge/cartridge_details.html"
    success_url = reverse_lazy('cartridge_list_instock')

# CartridgeProductNo. Views

class CartridgeProductNumberListView(LoginRequiredMixin, ListView):
    model = CartridgeProductNumber
    template_name = 'cartridge/cartridge_product_no/list_cartridge_product_no.html'
    context_object_name = 'cartridge_product_nos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = PrinterModelFilter(self.request.GET, queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = PrinterModelFilter(self.request.GET, queryset)
        context["cartridge_product_nos"] = filter
        return context

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

class LocationListView(LoginRequiredMixin, ListView):
    model = Location
    template_name = 'item_location/list_location.html'
    context_object_name = 'locations'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = LocationFilter(self.request.GET, queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = LocationFilter(self.request.GET, queryset)
        context["locations"] = filter
        return context

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

class MakeListView(LoginRequiredMixin, ListView):
    model = Make
    template_name = 'make/list_make.html'
    context_object_name = 'makes'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = MakeFilter(self.request.GET, queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = MakeFilter(self.request.GET, queryset)
        context["makes"] = filter
        return context

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

# Vendor Views

class VendorListView(LoginRequiredMixin, ListView):
    model = Vendor
    template_name = 'vendor/list_vendor.html'
    context_object_name =  'vendors'
    paginate_by: 20

    def get_queryset(self):
        queryset = super().get_queryset()
        filter = VendorFilter(self.request.GET, queryset)
        return filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        filter = VendorFilter(self.request.GET, queryset)
        context["vendors"] = filter
        return context

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
    template_name = "vendor/details_vendor.html"
    success_url = reverse_lazy('list_vendor')