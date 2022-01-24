from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.models import Group

from authentication.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email',
                    'is_active', 'is_staff', 'is_superuser',
                    'date_created', 'date_updated', 'group')
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')
                }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )


admin.site.unregister(Group)
