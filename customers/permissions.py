from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions

from .models import Customer

# from events.models import Event

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
DELETE_METHOD = ['DELETE']
POST_METHOD = ['POST']


class IsConcernedOrAdmin(permissions.BasePermission):
    """
    CUSTOMERS
    Allows rights to customers_instances in function of User.group.
    "GESTION" has superuser rights.
    "VENTE" can CREATE, READ all Customers and UPDATE Customers if they are linked with.
    "SUPPORT" can GET Customers-lists and GET Detail information of one if they are linked with.
    
    Only superusers can delete Customers and add a "VENTE" User to.
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
        
        # # Detail Access (GET) for "SUPPORT" member linked with customer by event.
        # try:
        #     event = Event.objects.get(customer_instance=view.kwargs.get(
        #         'pk'), support_contact=request.user.id)
        #     if request.method in SAFE_METHODS:
        #         return True
        # except ObjectDoesNotExist:
        #     return False
            
        
        
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff or request.user.group == "GESTION":
            return True
        
        if obj.sales_contact == request.user:
            return True
        
        # # Detail Access (GET) for "SUPPORT" member linked with customer by event.
        # try:
        #     event = Event.objects.get(customer_instance=view.kwargs.get(
        #         'pk'), support_contact=request.user.id)
        #     if request.method in SAFE_METHODS:
        #         return True
        # except ObjectDoesNotExist:
        #     return False
