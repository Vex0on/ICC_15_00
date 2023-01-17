from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'surname',
        'phoneNumber',
        'email',
        'pesel'
    ]


@admin.register(WorkerAddress)
class WorkerAddressAdmin(admin.ModelAdmin):
    list_display = [
        'worker',
        'street',
        'houseNumber',
        'flatNumber',
        'postcode',
        'placeName'
    ]


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    list_display = [
        'description',
        'startTime', 
        'endTime'
    ]


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'surname',
        'phoneNumber',
        'email',
        'pesel'
    ]


@admin.register(ClientAddress)
class ClientAddressAdmin(admin.ModelAdmin):
    list_display = [
        'client',
        'street',
        'houseNumber',
        'flatNumber',
        'postcode',
        'placeName'
    ]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'zone', 
        'client', 
        'price', 
        'worker'
    ]
