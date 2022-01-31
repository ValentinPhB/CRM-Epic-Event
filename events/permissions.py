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

        # Detail Access (GET, PUT) for "SUPPORT" member linked with current event.
        event = Event.objects.filter(pk=view.kwargs.get('pk')).first()
        if event and event.support_contact == request.user and request.method not in DELETE_METHOD:
            return True

        # Detail Access (GET, PUT) for "VENTE" member linked with contract of current event.
        if event:
            contract = Contract.objects.filter(
                pk=event.contract_instance.id).first()
            if contract and contract.sales_contact == request.user and request.method not in DELETE_METHOD:
                return True

        # Detail Access (GET, PUT) for "VENTE" member linked with customer of current event.
        if event:
            customer = Customer.objects.filter(
                pk=event.customer_instance.id).first()
            if customer and customer.sales_contact == request.user and request.method not in DELETE_METHOD:
                return True

    def has_object_permission(self, request, view, obj):
        if self.has_permission(request, view):
            return True
