
from datetime import datetime

from rest_framework import serializers

from .models import User


class UserListSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_superuser', 'date_created', 'date_updated', 'group')
        
class UserDetailSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    date_updated = serializers.DateTimeField(
        format="%d-%m-%Y %H:%M:%S", read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser',
                  'date_created', 'date_updated', 'password', 'group', 'assigned_customers')
        read_only_fields = ('assigned_customers',)
        
    def update(self, instance, validated_data):
        if validated_data.get('password') == instance.password:
            password = validated_data.pop('password')
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
