
from dataclasses import fields
from django.contrib import admin
from item.models import *

# Register your models here.
item_models = [Location,
               PrinterModel,
               CartridgeProductNumber,
               Make,
               Cartridge,
               Printer,
               Vendor,]

admin.site.register(item_models)