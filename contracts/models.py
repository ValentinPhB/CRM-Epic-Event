from django.db import models
from django.core import validators

from authentication.models import User
from customers.models import Customer


class Contract(models.Model):
    sales_contact = models.ForeignKey(User, verbose_name="Vendeur assigné",
                                      related_name="assigned_contract",
                                      on_delete=models.SET_DEFAULT, default=0, blank=True,
                                      null=True, limit_choices_to={'group': "VENTE"})
    customer_instance = models.ForeignKey(
        Customer, verbose_name="Client", related_name="contracts", on_delete=models.CASCADE)

    date_created = models.DateTimeField(
        verbose_name="Date de création", auto_now_add=True)
    date_updated = models.DateTimeField(
        verbose_name="Date de mise à jour", auto_now=True)
    status = models.BooleanField(verbose_name="Contrat signé ?", default=False)
    amount = models.FloatField(
        validators=[validators.MinValueValidator(0.1)], verbose_name="Coût")
    payment_due = models.DateTimeField(verbose_name="Date de paiement prévue")


    class Meta:
        verbose_name_plural = "Liste des contrats"
        verbose_name = "Contrats"


    def __str__(self):
        return 'Vendeur assigné : %s, Client : %s, État : %s, Date %s' % (self.sales_contact, self.customer_instance, self.status, self.payment_due,)
