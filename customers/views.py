from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Customer
from .permissions import IsConcernedOrAdmin
from .serializers import CustomerListSerializer, CustomerAdminSerializer, CustomerDetailSerializer


# Documentation is in french because it's displayed in the view.
class CustomerViewSet(viewsets.ModelViewSet):
    """
    ### [Documentation, Permissions, Filtering and Ordering. Select *Customer* folder.](https://documenter.getpostman.com/view/18470677/UVeDtTUR)\n
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerListSerializer
    detail_serializer_class = CustomerDetailSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['id', 'date_created',
                       'date_updated', 'sales_contact_id']
    search_fields = ['id', 'first_name', 'last_name', 'email',
                     'company_name', 'group', ]
    permission_classes = (IsAuthenticated, IsConcernedOrAdmin,)

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser or self.request.user.group == "GESTION":
            return CustomerAdminSerializer
        if self.action == 'list':
            return CustomerListSerializer
        if self.action in ['retrieve', 'create', 'update', 'delete']:
            return CustomerDetailSerializer
        return CustomerListSerializer
