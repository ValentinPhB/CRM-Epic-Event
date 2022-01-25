from django.forms import ModelForm, ValidationError

from .models import Customer


class CustomerAdminForm(ModelForm):
    """
    CustomerAdminForm to check if sales.contact is from "VENTE" group.
    """
    class Meta:
        model = Customer
        fields = '__all__'
        
    def clean_sales_contact(self):
        sales_contact = self.cleaned_data['sales_contact']
        if sales_contact.group != 'VENTE':
            raise ValidationError(
                "ATTENTION : Pour être affecté à ce client, ce professionnel doit être du groupe 'VENTE'.")
        return sales_contact
