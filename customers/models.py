from django.core.validators import RegexValidator
from django.db import models

from authentication.models import User


class Customer(models.Model):
    class GroupChoices(models.TextChoices):
        POTENTIAL = "POTENTIEL"
        EXISTING = "EXISTANT"
        
    sales_contact = models.ForeignKey(User, verbose_name="Vendeur assigné",
                                      related_name="assigned_customers", on_delete=models.SET_DEFAULT, default=0, blank=True, null=True, limit_choices_to={'group': "VENTE"})
    first_name = models.CharField(
        verbose_name="Prénom", max_length=150, blank=True)
    last_name = models.CharField(
        verbose_name="Nom de famille", max_length=150)
    email = models.EmailField(
        verbose_name="Email", max_length=150, unique=True)
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Le numéro de téléphone doit être rentré dans le format suivant: '+999999999'. 15 chiffres sont autorisés.")
   
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, verbose_name="Téléphone")
    mobile_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, verbose_name="Téléphone portable")
    
    company_name = models.CharField(max_length=250, blank=True, verbose_name="Entreprise")
    date_created = models.DateTimeField(
        verbose_name="Date de création", auto_now_add=True)
    date_updated = models.DateTimeField(
        verbose_name="Date de mise à jour", auto_now=True)
    group = models.CharField(max_length=100, choices=GroupChoices.choices, default=GroupChoices.POTENTIAL, verbose_name="Groupe")
         
    class Meta:
        verbose_name_plural = "Liste des clients"
        verbose_name = "Clients"
    
    def __str__(self):
        return '%s, %s, Vendeur assigné : %s, Groupe : %s' % (self.last_name, self.email, self.sales_contact, self.group)
