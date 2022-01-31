from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions

from .models import Event
from customers.models import Customer
from contracts.models import Contract


SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
DELETE_METHOD = ['DELETE']
POST_METHOD = ['POST']


class IsConcernedOrAdmin(permissions.BasePermission):
    """
    EVENT
    Allows rights to event_instances in function of User.group.
    "GESTION" has superuser rights.
    "VENTE" and "SUPPORT" can GET event_lists.
    "VENTE" can CREATE, READ DETAILS's Event and UPDATE it if they are linked with.
    "SUPPORT" can READ DETAILS's Event and UPDATE it if they are linked with.
    
    Only superusers can delete Event.
    """
    
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff or request.user.group == "GESTION":
            return True

        if request.method in SAFE_METHODS:
            return True

        if request.user.group == "VENTE" and request.method in POST_METHOD:
            return True

        # Detail Access (GET, PUT) for "VENTE" member linked with contract of current event,
        try:
            event = Event.objects.get(pk=view.kwargs.get('pk'))
            contract = Contract.objects.get(pk=event.contract_instance.id)
            if contract.sales_contact == request.user and request.method not in DELETE_METHOD:
                return True
            
            # If user is linked with customer by other contracts.
            other_contract = Contract.objects.filter(customer_instance=event.customer_instance)   
            if other_contract:
                for x in other_contract:
                    if x.sales_contact == request.user and request.method not in DELETE_METHOD:
                        return True
        except ObjectDoesNotExist:
            return False

        # Detail Access (GET, PUT) for "VENTE" member linked with customer of current event.
        try:
            event = Event.objects.get(pk=view.kwargs.get('pk'))
            customer = Customer.objects.get(pk=event.customer_instance.id)
            if customer.sales_contact == request.user and request.method not in DELETE_METHOD:
                return True
        except ObjectDoesNotExist:
            return False

        # Detail Access (GET, PUT) for "SUPPORT" member linked with current event.
        try:
            event = Event.objects.get(pk=view.kwargs.get('pk'))
            if event.support_contact == request.user and request.method not in DELETE_METHOD:
                return True
        except ObjectDoesNotExist:
            return False


    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff or request.user.group == "GESTION":
            return True
    
        if obj.support_contact == request.user:
            return True
        
        # Detail Access (GET, PUT) for "VENTE" member linked with contract of current event,
        try:
            contract = Contract.objects.get(pk=obj.contract_instance.id)
            if contract.sales_contact == request.user:
                return True

            # If user is linked with customer by other contracts.
            other_contract = Contract.objects.filter(
                customer_instance=obj.customer_instance.id)
            if other_contract:
                for x in other_contract:
                    if x.sales_contact == request.user:
                        return True
        except ObjectDoesNotExist:
            return False

        # Detail Access (GET, PUT) for "VENTE" member linked with customer of current event.
        try:
            customer = Customer.objects.get(pk=obj.customer_instance.id)
            if customer.sales_contact == request.user:
                return True
        except ObjectDoesNotExist:
            return False
