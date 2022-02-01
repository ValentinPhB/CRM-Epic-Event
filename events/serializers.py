from datetime import datetime

from rest_framework import serializers

from authentication.models import User
from .models import Event


class EventBaseSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    event_date = serializers.DateField(
        format="%d-%m-%Y")

    readable_customer_instance = serializers.CharField(
        source='customer_instance', read_only=True)
    readable_contract_instance = serializers.CharField(
        source='contract_instance', read_only=True)
    readable_support_contact = serializers.CharField(
        source='support_contact', read_only=True)
    
    def validate_support_contact(self, value):
        """
        Check if user is from group named "SUPPORT".
        """
        if value:
            user_instance = User.objects.get(pk=value.id)
            if user_instance.group != "SUPPORT":
                raise serializers.ValidationError(
                    "ATTENTION : Pour être affecté à ce client, ce professionnel doit être du groupe 'SUPPORT'.")
            return value

    def validate_event_date(self, value):
        """
        Check if 'event_date' and if 'event_date > datetime.now for create or update.
        """
        date_now = datetime.now().strftime("%Y-%m-%d")

        # Update
        if self.instance and value:
            if value.strftime("%Y-%m-%d") == '1900-01-01':
                return self.instance.event_date

            if value.strftime("%Y-%m-%d") != '1900-01-01' and value.strftime("%Y-%m-%d") < date_now:
                raise serializers.ValidationError(
                    "ATTENTION : Une date antérieure à celle du jour actuel ne peut être selectionnée.")
        #create
        elif not self.instance and value:
            if value.strftime("%Y-%m-%d") == '1900-01-01':
                return None

            if value.strftime("%Y-%m-%d") != '1900-01-01' and value.strftime("%Y-%m-%d") < date_now:
                raise serializers.ValidationError(
                    "ATTENTION : Une date antérieure à celle du jour actuel ne peut être selectionnée.")
        return value

class EventListSerializer(EventBaseSerializer):
    class Meta:
        model = Event
        fields = ('id', 'readable_customer_instance', 'readable_contract_instance',
                  'readable_support_contact', 'date_created', 'date_updated',
                  'event_status', 'event_date',)

class EventDetailSerializer(EventBaseSerializer):
    class Meta:
        model = Event
        fields = ('id', 'readable_customer_instance', 'readable_contract_instance',
                  'readable_support_contact','customer_instance', 'contract_instance',
                  'date_created', 'date_updated', 'event_status', 'attendees',
                  'event_date', 'notes',)

class EventAdminSerializer(EventBaseSerializer):

    class Meta:
        model = Event
        fields = ('id', 'readable_customer_instance', 'readable_contract_instance',
                  'readable_support_contact','customer_instance', 'contract_instance',
                  'support_contact', 'date_created', 'date_updated', 'event_status',
                  'attendees', 'event_date', 'notes',)
