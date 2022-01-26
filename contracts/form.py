from django.forms import ModelForm, ValidationError

from .models import Contract


class ContractAdminForm(ModelForm):
    """
    ContractAdminForm to check if sales.contact is from "VENTE" group and if 'payement due' > date.now().
    """
    class Meta:
        model = Contract
        fields = '__all__'

    def clean_sales_contact(self):
        sales_contact = self.cleaned_data['sales_contact']
        if sales_contact.group != 'VENTE':
            raise ValidationError(
                "ATTENTION : Pour être affecté à ce client, ce professionnel doit être du groupe 'VENTE'.")
        return sales_contact

    def clean_payment_due(self):
        payment_due = self.cleaned_data['payment_due']
        date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if payment_due.strftime("%Y-%m-%d %H:%M:%S") < date_now:
            raise ValidationError(
                "ATTENTION : Une date antérieure à celle du jour actuel ne peut être selectionnée.")
        return payment_due
