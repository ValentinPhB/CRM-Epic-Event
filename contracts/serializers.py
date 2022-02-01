from datetime import datetime

from rest_framework import serializers

from authentication.models import User
from .models import Contract

class ContractBaseSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    payment_due = serializers.DateField(
        format="%d-%m-%Y")
    
    readable_sales_contact = serializers.CharField(
        source='sales_contact', read_only=True)
    readable_customer_instance = serializers.CharField(
        source='customer_instance', read_only=True)

    events_linked = serializers.SlugRelatedField(many=True, read_only=True,
                                                 slug_field='readable_reverse_key')
    
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
        Check if 'payment_due' and if 'payment_due' > datetime.now for create or update.
        """
        date_now = datetime.now().strftime("%Y-%m-%d")

        # Update
        if self.instance and value:
            if value.strftime("%Y-%m-%d") == '1900-01-01':
                return self.instance.payment_due

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


class ContractListSerializer(ContractBaseSerializer):  
    class Meta:
        model = Contract
        fields = ('id', 'readable_sales_contact', 'readable_customer_instance',
                  'date_created', 'date_updated','status', 'amount',
                  'payment_due',)
        
        
class ContractDetailSerializer(ContractBaseSerializer): 
    class Meta:
        model = Contract
        fields = ('id', 'readable_sales_contact', 'readable_customer_instance',
                  'sales_contact', 'customer_instance', 'date_created',
                  'date_updated', 'status', 'amount', 'payment_due', 'events_linked')
