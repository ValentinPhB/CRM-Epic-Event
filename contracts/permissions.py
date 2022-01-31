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

        # Detail Access (GET, PUT) for "VENTE" member linked with customer_instance of current contract.
        contract = Contract.objects.filter(pk=view.kwargs.get('pk')).first()
        if contract and contract.sales_contact == request.user and request.method not in DELETE_METHOD:
            return True

        # Detail Access (GET, PUT) for "VENTE" member linked with customer_instance (Prospect function).
        if contract:
            customer = Customer.objects.filter(
                pk=contract.customer_instance.id).first()
            if customer.sales_contact == request.user and request.method not in DELETE_METHOD:
                return True

    def has_object_permission(self, request, view, obj):
        if self.has_permission(request, view):
            return True
