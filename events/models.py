from django.db import models
from django.core import validators

from customers.models import Customer
from contracts.models import Contract
from authentication.models import User


class Event(models.Model):
    class EventSatuts(models.TextChoices):
        DEVELOPMENT = "EN PRÉPARATION"
        READY = "PRÊT"
        CANCEL = "ANNULÉ"

    customer_instance = models.ForeignKey(
        Customer, verbose_name="Client", related_name="events", on_delete=models.CASCADE)
    contract_instance = models.ForeignKey(
        Contract, verbose_name="Contrat", related_name="events_linked", on_delete=models.CASCADE)
    support_contact = models.ForeignKey(User, verbose_name="Membre support assigné",
                                        related_name="assigned_events", on_delete=models.SET_DEFAULT, default=None,
                                        blank=True, null=True, limit_choices_to={'group': "SUPPORT"})

    date_created = models.DateTimeField(
        verbose_name="Date de création", auto_now_add=True)
    date_updated = models.DateTimeField(
        verbose_name="Date de mise à jour", auto_now=True)
    event_status = models.CharField(max_length=100, verbose_name="Status de l'évènement",
                                    choices=EventSatuts.choices, default=EventSatuts.DEVELOPMENT)
    attendees = models.IntegerField(
        validators=[validators.MinValueValidator(1)], verbose_name="Nombre d'invités", blank=True, null=True)
    event_date = models.DateField(verbose_name="Date de l'évènement", null=True, blank=True)
    notes = models.TextField(verbose_name="Commentaires", blank=True)

    class Meta:
        verbose_name_plural = "Liste des évènements"
        verbose_name = "évènements"

    def __str__(self):
        if self.support_contact:
            return 'ID: %s, Client : %s, Support : %s' % (self.id, self.customer_instance.email, self.support_contact.email)
        return 'ID: %s, Client : %s, Support : AUCUN' % (self.id, self.customer_instance.email)

    @property
    def readable_reverse_key(self):
        if self.support_contact:
            return 'ID: %s, Client : %s, Support : %s' % (self.id, self.customer_instance.email, self.support_contact.email)
        return 'ID: %s, Client : %s, Support : AUCUN' % (self.id, self.customer_instance.email)
