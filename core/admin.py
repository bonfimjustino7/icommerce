from django.contrib import admin

from core.models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    pass


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    readonly_fields = ('amount',)
