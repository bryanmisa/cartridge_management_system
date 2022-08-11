
from pyexpat import model
from django.conf import settings
from django.db import models


# Create your models here.

class Item(models.Model):                                               # Base or Parent Class for CMS models 
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)        
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True





class Location(Item):
    # Location class will determin the location of the Item Created
    pass
    class Meta:
        ordering = ['name']




class PrinterModel(Item):
    # The PrinterModel will be used to link the Cartridge and the Printer.
    pass
    class Meta:
        ordering = ['-updated_at']



class CartridgeProductNumber(Item):  

    # CartridgeProductNumber will be the base to count 
    # how many cartridges that is linked on to the CartridgeProductNumber.

    CARTRIDGE_TYPE = (                          # Type of Cartridges
        ('Ink', 'Ink'),
        ('Toner', 'Toner'),
    )

    COLOR = (
        ('Black', 'Black'),
        ('Yellow', 'Yellow'),
        ('Mangenta', 'Magenta'),
        ('Cyan', 'Cyan'),
    )

    color =  models.CharField(max_length=10, 
                             choices=COLOR,
                             default='')
    cartridge_type = models.CharField(max_length=10, 
                                      choices=CARTRIDGE_TYPE,
                                      default='')

class Make(Item):
    # Make or the Manufacturer of the Item
    pass
    class Meta:
        ordering = ['-updated_at']

class Cartridge(Item):
    # Cartridge Model will hold the important values as the below 
    STATUS_CHOICES = (
        ('In Stock', 'In Stock'),
        ('Installed' , 'Installed'),
        ('Disposed', 'Disposed'),
    )

    status = models.CharField(max_length=10,                        # This field will on only show when installing
                              choices=STATUS_CHOICES,               # the cartridge 
                              default='In Stock')

    printer =  models.ForeignKey('Printer',                         # Foreign Key for Printer 
                                on_delete=models.CASCADE, 
                                null=True, 
                                blank=True,default='')

    printer_model = models.ForeignKey('PrinterModel',               # Foreign Key for Printer Model this is to be
                                      on_delete=models.SET_DEFAULT, # used for linking the printer and the cartridge
                                      blank=True,
                                      default='')

    make = models.ForeignKey('Make',on_delete=models.SET_NULL,      # Foreign Key for Models Make
                                    blank=True, null=True)

                                
    cart_prod_no = models.ForeignKey('CartridgeProductNumber',       # this is to be linked with CatridgeProductNumber to 
                                     on_delete=models.SET_DEFAULT,   # get the query on how many cartridges are there
                                     null=True,                      # under the assigned CartridgeProductNumber
                                     blank=True,
                                     default='', related_name='cart_prod_no')

    installed_date = models.DateField(blank=True, null=True)          # this field will only show when installing the 
                                                                      # cartridge
    
    date_received = models.DateField(blank=True, null=True)           # field will only show when creating the the model

    date_disposed = models.DateField(blank=True, null=True)           # field will only show when disposing the the model

    vendor = models.ForeignKey('Vendor',                              # Vendor will provide the information where to order 
                                on_delete=models.SET_NULL,            # the cartridges
                                null=True, 
                                blank=True)
    
    class Meta:
        ordering = ['-updated_at']

class Printer(Item):
    

    asset_tag = models.CharField(max_length=100,                    # this will provide the Asset tag of the printer
                                blank=True, 
                                unique=True)

    serial_number = models.CharField(max_length=100,                # to get the correct info of the printer that can be provided 
                                    blank=True,                     # to the vendor
                                    unique=True)
                                    
    location = models.ForeignKey('Location',                        # to know the location of the printer          
                                 on_delete=models.SET_NULL, 
                                 null=True, 
                                 blank=True)

    printer_model = models.ForeignKey('PrinterModel',               # this foreignkey will link to the PrinterModel, so that
                                      on_delete=models.SET_NULL,    # the cartridges assigned on the same PrinterModel can provide
                                      null=True, blank=True)        # the querysets against the cartrigdes assigned on the Printer.

    make = models.ForeignKey('Make',                                # Manufacturer or Make
                            on_delete=models.SET_NULL, 
                            null=True, 
                            blank=True)

    vendor = models.ForeignKey('Vendor',                            # Details of the Printer Provider.
                            on_delete=models.SET_NULL, 
                            null=True, 
                            blank=True)

    class Meta:
        ordering = ['-updated_at']

class Vendor(models.Model):                                         # Vendor Details

    company_name = models.CharField(max_length=100, 
                                blank=True, 
                                unique=True)
    contact_person =  models.CharField(max_length=100)
    company_contact_number = models.CharField(max_length=50)
    notes_on_vendor = models.TextField()

    def __str__(self):                  # Return the name of the Vendor
        return self.company_name

