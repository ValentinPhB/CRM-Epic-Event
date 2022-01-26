from datetime import datetime

from rest_framework import serializers

from authentication.models import User
from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    payment_due = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S")
    
    class Meta:
        model = Contract
        fields = ('id', 'sales_contact', 'customer_instance', 'date_created', 'date_updated', 'status', 'amount', 'payment_due')
        
    def validate_sales_contact(self, value):
        """
        Check if user is from group named "VENTE".
        """
        if value:
            user_instance = User.objects.get(pk=value.id)
            if user_instance.group != "VENTE":
                raise serializers.ValidationError(
                    "ATTENTION : Pour être affecté à ce client, ce professionnel doit être du groupe 'VENTE'.")
            return value
        
    def validate_payment_due(self, value):
        """
        Check if 'payment_due' > datetime.now.
        """
        if value:
            date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if value.strftime("%Y-%m-%d %H:%M:%S") < date_now:
                raise serializers.ValidationError(
                    "ATTENTION : Une date antérieure à celle du jour actuel ne peut être selectionnée.")
            return value
    
