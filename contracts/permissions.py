from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions

from .models import Contract
from customers.models import Customer


SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
DELETE_METHOD = ['DELETE']
POST_METHOD = ['POST']


class IsConcernedOrAdmin(permissions.BasePermission):
    """
    CONTRACT
    Allows rights to contract_instances in function of User.group.
    "GESTION" members has superuser rights.
    "VENTE" members and "SUPPORT" can GET Contracts_lists.
    "VENTE" members can CREATE, READ DETAIL's Contract and UPDATE it if they are linked with.
    
    Only superusers can delete Contract.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff or request.user.group == "GESTION":
            return True

        if request.method in SAFE_METHODS:
            return True

        if request.user.group == "VENTE" and request.method in POST_METHOD:
            return True

        # Detail Access (GET, PUT) for "VENTE" member linked with contract.
        try:
            contract = Contract.objects.get(pk=view.kwargs.get('pk'))
            if contract.sales_contact == request.user and request.method not in DELETE_METHOD:
                return True
        except ObjectDoesNotExist:
            return False
        
        # Detail Access (GET, PUT) for "VENTE" member linked with customer.
        try:
            contract = Contract.objects.get(pk=view.kwargs.get('pk'))
            customer = Customer.objects.get(pk=contract.customer_instance.id)
            if customer.sales_contact == request.user and request.method not in DELETE_METHOD:
                return True
        except ObjectDoesNotExist:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff or request.user.group == "GESTION":
            return True

        if obj.sales_contact == request.user:
            return True

        # Detail Access (GET, PUT) for "VENTE" member linked with customer.
        try:
            customer = Customer.objects.get(pk=obj.customer_instance.id)
            if customer.sales_contact == request.user:
                return True
        except ObjectDoesNotExist:
            return False
