from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions

from .models import Customer
from events.models import Event
from contracts.models import Contract

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
DELETE_METHOD = ['DELETE']
POST_METHOD = ['POST']


class IsConcernedOrAdmin(permissions.BasePermission):
    """
    CUSTOMERS
    Allows rights to customers_instances in function of User.group.
    "GESTION" has superuser rights.
    "VENTE" and "SUPPORT" can GET customers_lists.
    "VENTE" can CREATE, READ DETAIL's Customers and UPDATE it if they are linked with.
    "SUPPORT" can GET Detail information of customers if they are linked with.
    
    Only superusers can delete Customers and add a "VENTE" User to customers.
    """
    
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff or request.user.group == "GESTION":
            return True

        if request.method in SAFE_METHODS:
            return True
        
        if request.user.group == "VENTE" and request.method in POST_METHOD:
            return True

        # Detail Access (GET, PUT) for "VENTE" member linked with customer.
        try:
            customer = Customer.objects.get(pk=view.kwargs.get('pk'))
            if customer.sales_contact == request.user and request.method not in DELETE_METHOD:
                return True
        except ObjectDoesNotExist:
            return False
        
        # Detail Access (GET, PUT) for "VENTE" member linked with customer by contract.
        try:
            customer = Customer.objects.get(pk=view.kwargs.get('pk'))
            other_contract = Contract.objects.filter(customer_instance=customer.id)
            if other_contract:
                for x in other_contract:
                    if x.sales_contact == request.user and request.method not in DELETE_METHOD:
                        return True
        except ObjectDoesNotExist:
            return False
        
        # Detail Access (GET) for "SUPPORT" member linked with customer by event.
        try:
            event = Event.objects.get(customer_instance=view.kwargs.get(
                'pk'), support_contact=request.user.id)
            if request.method in SAFE_METHODS:
                return True
        except ObjectDoesNotExist:
            return False
            
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff or request.user.group == "GESTION":
            return True
        
        if obj.sales_contact == request.user:
            return True
        
        # Detail Access (GET) for "SUPPORT" member linked with customer by event.
        try:
            event = Event.objects.get(customer_instance=obj.id, support_contact=request.user.id)
            return True
        except ObjectDoesNotExist:
            return False

        # Detail Access (GET, PUT) for "VENTE" member linked with customer by contract.
        try:
            other_contract = Contract.objects.filter(
                customer_instance=obj.id)
            if other_contract:
                for x in other_contract:
                    if x.sales_contact == request.user:
                        return True
        except ObjectDoesNotExist:
            return False
