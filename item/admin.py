
from dataclasses import fields
from django.contrib import admin
from item.models import *

# List of created Item Models

item_models = [Location,
               PrinterModel,
               CartridgeProductNumber,
               Make,
               Cartridge,
               Printer,
               Vendor,]

admin.site.register(item_models)