from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Event
from .permissions import IsConcernedOrAdmin
from .serializers import EventListSerializer, EventDetailSerializer, EventAdminSerializer


# Documentation is in french because it's displayed in the view.
class EventViewSet(viewsets.ModelViewSet):
    """
    ### [Documentation, Permissions, Filtering and Ordering. Select *Event* folder.](https://documenter.getpostman.com/view/18470677/UVeDtTUR)\n
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
