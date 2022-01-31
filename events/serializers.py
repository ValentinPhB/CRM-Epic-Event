from datetime import datetime

from rest_framework import serializers

from authentication.models import User
from .models import Event


class EventListSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    event_date = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S")

    readable_customer_instance = serializers.CharField(
        source='customer_instance', read_only=True)
    readable_contract_instance = serializers.CharField(
        source='contract_instance', read_only=True)
    readable_support_contact = serializers.CharField(
        source='support_contact', read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'readable_customer_instance', 'readable_contract_instance', 'readable_support_contact',
                  'date_created', 'date_updated', 'event_status', 'event_date',)


class EventDetailSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    event_date = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S")

    readable_customer_instance = serializers.CharField(
        source='customer_instance', read_only=True)
    readable_contract_instance = serializers.CharField(
        source='contract_instance', read_only=True)
    readable_support_contact = serializers.CharField(
        source='support_contact', read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'readable_customer_instance', 'readable_contract_instance', 'readable_support_contact',
                  'customer_instance', 'contract_instance', 'support_contact',
                  'date_created', 'date_updated', 'event_status', 'attendees',
                  'event_date', 'notes',)

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
        Check if 'event_date' > datetime.now.
        """
        if value:
            date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if value.strftime("%Y-%m-%d %H:%M:%S") < date_now:
                raise serializers.ValidationError(
                    "ATTENTION : Une date antérieure à celle du jour actuel ne peut être selectionnée.")
            return value
