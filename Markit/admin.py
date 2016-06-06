from django.contrib import admin
from .models import System
from .models import Stock

class SystemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

admin.site.register(System, SystemAdmin)

class StockAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'file']

admin.site.register(Stock, StockAdmin)