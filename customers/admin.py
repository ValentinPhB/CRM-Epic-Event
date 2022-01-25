from django.contrib import admin

from .models import Customer
from .form import CustomerAdminForm


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    CustomerAdminForm to check if sales.contact is from "VENTE" group.
    """
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone_number', 'mobile_number', 'company_name',
                    'date_created', 'date_updated', 'group', 'sales_contact')

    search_fields = ['id', 'first_name', 'last_name', 'email', 'company_name', 'group',]
    form = CustomerAdminForm
