from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Contract
from .permissions import IsConcernedOrAdmin
from .serializers import ContractListSerializer, ContractDetailSerializer


# Documentation is in french because it's displayed in the view.
class ContractViewSet(viewsets.ModelViewSet):
    """
    La recherche est sensible aux attributs suivants : 'id', 'status'(BOOL).\n
    Les éléments peuvent être ordonnés pour les attributs suivants :'id', 'sales_contact_id', 'customer_instance_id', 'amount', 'date_created', 'date_updated', 'payment_due'.\n
    Seuls les "supers-utilisateurs" peuvent supprimer une instance.\n
    Les membres de l'équipe "VENTE" peuvent créer un contrat.\n
    Les membres de l'équipe "VENTE" et "SUPPORT" peuvent avoir accès, en lecture, à la liste générale des contrats.\n
    Les membres de l'équipe "VENTE" peuvent avoir accès au détail d'un contract et en modifier ses attributs si il lui est affilié ou s'il est affilié au client.
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
