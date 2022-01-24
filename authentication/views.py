from django.contrib.auth.hashers import make_password

from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import User
from .permissions import IsAdminUser
from .serializers import UserListSerializer, UserDetailSerializer


    
class UserViewSet(viewsets.ModelViewSet):
    """
    L'affichage et les actions sont déterminés par votre niveau de droits concernant les utilisateurs.\n
    La recherche est sensible aux attributs : 'id', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'group'.\n
    Seuls les supers-utilisateurs, staff-membres et membres de groupe "GESTION" peuvent ajouter, modifier ou supprimer un utilisateur.\n
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['id', 'first_name', 'last_name', 'email', 'is_staff', 'is_superuser', 'group']
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
        if self.action == 'list':
            return UserListSerializer
        elif self.action in ['retrieve', 'update', 'create', 'delete']:
            return UserDetailSerializer
        return UserListSerializer
