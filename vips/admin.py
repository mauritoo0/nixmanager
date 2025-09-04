from django.contrib import admin
from .models import *

# Register your models here.

# ----------------- PROMOTERS -----------------
class PromoterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'area', 'phone', 'user')
    search_fields = ('first_name', 'last_name', 'area', 'phone', 'user')

admin.site.register(Promoter, PromoterAdmin)

# ----------------- CUSTOMERS -----------------
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'address', 'city', 'phone', 'email', 'promoter', 'user')
    search_fields = ('first_name', 'last_name', 'address', 'city', 'phone', 'email', 'promoter', 'user')

admin.site.register(Customer, CustomerAdmin)

# ----------------- TABLES -----------------
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'price')
    search_fields = ('number', 'capacity', 'price')

admin.site.register(Table, TableAdmin)

# ----------------- RESERVATIONS -----------------
class ReservationAdmin(admin.ModelAdmin):

    def date_formatted(self, obj):
        return obj.date.strftime('%d/%m/%Y')
    date_formatted.short_description = 'Date'

    list_display = ('customer', 'table', 'guests', 'date_formatted', 'promoter', 'user')
    search_fields = ('customer', 'table', 'guests', 'date_formatted', 'promoter', 'user')

admin.site.register(Reservation, ReservationAdmin)