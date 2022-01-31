from django.contrib import admin

from .models import Contract
from .form import ContractAdminForm


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """
    ContractAdminForm to check if sales.contact is from "VENTE" group and if 'payement due' > date.now().
    """
    list_display = ('id', 'sales_contact', 'customer_instance', 'date_created',
                    'date_updated', 'status', 'amount', 'payment_due')

    search_fields = ['id', 'status', ]
    form = ContractAdminForm
