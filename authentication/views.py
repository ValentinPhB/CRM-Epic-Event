from django.contrib.auth.hashers import make_password

from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import User
from .permissions import IsAdminUser
from .serializers import UserListSerializer, UserDetailSerializer


# Documentation is in french because it's displayed in the view.
class UserViewSet(viewsets.ModelViewSet):
    """
    ### [Documentation, Permissions, Filtering and Ordering. Select *User* folder.](https://documenter.getpostman.com/view/18470677/UVeDtTUR)\n
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['id', 'date_created', 'date_updated']
    search_fields = ['id', 'first_name', 'last_name', 'email',
                     'is_superuser', 'group']
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def perform_create(self, serializer):
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            user = serializer.save(password=password)
        else:
            user = serializer.save()
        if user.is_staff or user.is_superuser:
            user.group = "GESTION"

    def get_serializer_class(self):
        if self.request.user.is_staff or self.request.user.is_superuser or self.request.user.group == "GESTION":
            return UserDetailSerializer
        return UserListSerializer
