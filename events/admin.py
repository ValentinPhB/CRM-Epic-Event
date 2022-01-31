from django.contrib import admin

from .models import Event
from .form import EventAdminForm


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    EventAdminForm to check if support_contact is from "SUPPORT" group and if 'event_date' > date.now().
    """
    list_display = ('id', 'customer_instance', 'contract_instance', 'support_contact',
                    'date_created', 'date_updated', 'event_status', 'attendees',
                    'event_date', 'notes',)

    search_fields = ['id', 'event_status', ]
    form = EventAdminForm
