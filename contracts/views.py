from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Contract
from .permissions import IsConcernedOrAdmin
from .serializers import ContractSerializer


# Documentation is in french because it's displayed in the view.
class ContractViewSet(viewsets.ModelViewSet):
    """
    La recherche est sensible aux attributs suivants : 'id', 'status'.\n
    Les éléments peuvent être ordonnés pour les attributs suivants :'id', 'date_created', 'date_updated', 'sales_contact_id', 'customer_instance_id', 'amount', 'payment_due'.\n
    Seuls les "supers-utilisateurs" peuvent supprimer une instance.\n
    Les membres de l'équipe "VENTE" et "SUPPORT" peuvent avoir accès, en lecture, à la liste générale des contrats.\n
    Les membres de l'équipe "VENTE" peuvent avoir accès au détail d'un contract et en modifier ses attributs si il lui est affilié ou s'il est affilié au client.\n
    """
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    detail_serializer_class = ContractSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['id', 'date_created', 'date_updated',
                       'sales_contact_id', 'customer_instance_id', 'amount', 'payment_due' ]
    search_fields = ['id', 'status', ]
    permission_classes = (IsAuthenticated, IsConcernedOrAdmin,)
