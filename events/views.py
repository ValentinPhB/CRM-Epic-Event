from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Event
from .permissions import IsConcernedOrAdmin
from .serializers import EventListSerializer, EventDetailSerializer, EventAdminSerializer


# Documentation is in french because it's displayed in the view.
class EventViewSet(viewsets.ModelViewSet):
    """
    La recherche est sensible aux attributs suivants : 'id(Event)','event_status'(BOOL).\n
    Les éléments peuvent être ordonnés pour les attributs suivants :'id(Event)', 'customer_instance_id', 'contract_instance_id', date_created', 'date_updated', 'support_contact_id', 'event_date', \n
    **Ordonner l'attribut 'support_contact_id' permet de mettre en évidence les évènements non affectés à un membre de l'équipe "SUPPORT"**.\n
    Seuls les "supers-utilisateurs" peuvent supprimer une instance.\n
    Les membres de l'équipe "VENTE" peuvent créer un évènement.\n
    Les membres de l'équipe "VENTE" et "SUPPORT" peuvent avoir accès, en lecture, à la liste générale des évènements.\n
    Les membres de l'équipe "VENTE" et "SUPPORT" peuvent avoir accès au détail d'un évènement et en modifier ses attributs si ils sont affiliés au client correspondant.\n
    """
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    detail_serializer_class = EventDetailSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['id', 'customer_instance_id', 'contract_instance_id',
                       'date_created', 'date_updated', 'support_contact_id', 'event_date', ]
    search_fields = ['id', 'event_status', ]
    permission_classes = (IsAuthenticated, IsConcernedOrAdmin,)

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser or self.request.user.group == "GESTION":
            return EventAdminSerializer
        if self.action == 'list':
            return EventListSerializer
        if self.action in ['retrieve', 'create', 'update', 'delete']:
            return EventDetailSerializer
        return EventListSerializer
