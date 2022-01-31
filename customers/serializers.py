from rest_framework import serializers

from .models import Customer
from authentication.models import User


class CustomerListSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    readable_sales_contact = serializers.CharField(
        source='sales_contact', read_only=True)
    
    class Meta:
        model = Customer
        fields = ('id', 'readable_sales_contact', 'first_name', 'last_name',
                  'date_created', 'date_updated',
                  'email', 'phone_number', 'mobile_number',
                  'company_name', 'group', )


class CustomerDetailSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    
    readable_sales_contact = serializers.CharField(
        source='sales_contact', read_only=True)
    
    events = serializers.SlugRelatedField(many=True, read_only=True,
                                          slug_field='readable_reverse_key', allow_null=True)
    contracts = serializers.SlugRelatedField(many=True, read_only=True,
                                             slug_field='readable_reverse_key', allow_null=True)
    
    class Meta:
        model = Customer
        fields = ('id', 'readable_sales_contact', 'first_name', 'last_name',
                  'email', 'phone_number', 'mobile_number', 'company_name',
                  'date_created', 'date_updated', 'group', 'events', 'contracts')

    
class CustomerAdminSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    
    readable_sales_contact = serializers.CharField(
        source='sales_contact', read_only=True)
    
    events = serializers.SlugRelatedField(many=True, read_only=True,
                                          slug_field='readable_reverse_key')
    contracts = serializers.SlugRelatedField(many=True, read_only=True,
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

    class Meta:
        model = Customer
        fields = ('id', 'readable_sales_contact', 'sales_contact', 'first_name', 'last_name',
                  'email', 'phone_number', 'mobile_number', 'company_name',
                  'date_created', 'date_updated', 'group', 'events', 'contracts')

