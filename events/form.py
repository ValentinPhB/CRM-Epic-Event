from datetime import datetime

from django.forms import ModelForm, ValidationError, DateField

from .models import Event


class EventAdminForm(ModelForm):
    """
    EventAdminForm to check if support_contact is from "SUPPORT" group and if 'event_date' > date.now().
    """
    class Meta:
        model = Event
        fields = '__all__'

    def clean_support_contact(self):
        support_contact = self.cleaned_data['support_contact']
        if support_contact and support_contact.group != 'SUPPORT':
            raise ValidationError(
                "ATTENTION : Pour être affecté à ce client, ce professionnel doit être du groupe 'SUPPORT'.")
        return support_contact

    def clean_event_date(self):
        event_date = self.cleaned_data['event_date']
        date_now = datetime.now().strftime("%Y-%m-%d")
        if event_date and event_date.strftime("%Y-%m-%d") < date_now:
            raise ValidationError(
                "ATTENTION : Une date antérieure à celle du jour actuel ne peut être selectionnée.")
        return event_date
