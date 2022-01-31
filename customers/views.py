from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Customer
from .permissions import IsConcernedOrAdmin
from .serializers import CustomerListSerializer, CustomerAdminSerializer, CustomerDetailSerializer


# Documentation is in french because it's displayed in the view.
class CustomerViewSet(viewsets.ModelViewSet):
    """
    La recherche est sensible aux attributs suivants : 'id(Customer)', 'first_name', 'last_name', 'email', 'company_name', 'group'.\n
    Les éléments peuvent être ordonnés pour les attributs suivants :'id(Customer)', 'date_created', 'date_updated', 'sales_contact_id'\n
    **Ordonner l'attribut 'sales_contact_id' permet de mettre en évidence les clients non affectés à un membre de l'équipe "VENTE"**.\n
    Seuls les "supers-utilisateurs" peuvent affecter une membre de l'équipe "VENTE" à un Client et supprimer une instance.\n
    Les membres de l'équipe "VENTE" et "SUPPORT" peuvent avoir accès, en lecture, à la liste générale des clients.\n
    Les membres de l'équipe "VENTE" peuvent avoir accès au détail d'un client et en modifier ses attributs si et seulement si, il lui est affilié.\n
    Les membres de l'équipe "SUPPORT" peuvent avoir accès au détail d'un client (lecture) si et seulement si, il lui est affilié par l'intermédiaire d'un évènement.
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
