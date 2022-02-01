from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Contract
from .permissions import IsConcernedOrAdmin
from .serializers import ContractListSerializer, ContractDetailSerializer


# Documentation is in french because it's displayed in the view.
class ContractViewSet(viewsets.ModelViewSet):
    """
    ### [Documentation, Permissions, Filtering and Ordering. Select *Contract* folder.](https://documenter.getpostman.com/view/18470677/UVeDtTUR)\n
    """
    queryset = Contract.objects.all()
    serializer_class = ContractListSerializer
    detail_serializer_class = ContractDetailSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['id', 'sales_contact_id', 'customer_instance_id',
                       'amount', 'date_created', 'date_updated', 'payment_due']
    search_fields = ['id', 'status', ]
    permission_classes = (IsAuthenticated, IsConcernedOrAdmin,)

    def get_serializer_class(self):
        if self.action == 'list':
            return ContractListSerializer
        if self.action in ['retrieve', 'create', 'update', 'delete']:
            return ContractDetailSerializer
        return ContractListSerializer
