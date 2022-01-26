from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password):
        if email is None:
            raise TypeError("Une adresse email est requise")
        user = self.model(email=self.normalize_email(email),
                          first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password):
        if email is None:
            raise TypeError("Une adresse email est requise")
        user = self.create_user(
            email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.group = "GESTION"
        user.save()
        return user

    def create_staffuser(self, email, first_name, last_name, password):
        if email is None:
            raise TypeError("Une adresse email est requise")

        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = False
        user.is_staff = True
        user.group = "GESTION"
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Groups(models.TextChoices):
        NON_ASSIGNED = "NON ASSIGNÉ"
        GESTION = "GESTION"
        VENTE = "VENTE"
        SUPPORT = "SUPPORT"

    first_name = models.CharField(
        verbose_name="Prénom", max_length=150)
    last_name = models.CharField(
        verbose_name="Nom de famille", max_length=150)
    email = models.EmailField(
        verbose_name="Email", max_length=150, unique=True)

    is_active = models.BooleanField(verbose_name="Actif ?", default=True)
    is_staff = models.BooleanField(
        verbose_name="Membre du Staff ?", default=False)
    is_superuser = models.BooleanField(
        verbose_name="Super-utilisateur ?", default=False)
    date_created = models.DateTimeField(
        verbose_name="Date de création", auto_now_add=True)
    date_updated = models.DateTimeField(
        verbose_name="Date de mise à jour", auto_now=True)
    group = models.CharField(
        verbose_name="Groupe", max_length=150, choices=Groups.choices, default=Groups.NON_ASSIGNED)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name_plural = "Gestion des utilisateurs"
        verbose_name = "Utilisateur"

    def __str__(self):
        return '%s, %s, %s, %s' % (self.id, self.first_name, self.last_name, self.email,)

    @property
    def get_full_name(self):
        return '%s, %s, %s' % (self.first_name, self.last_name, self.email,)

    @property
    def get_short_name(self):
        return '%s, %s' % (self.first_name, self.last_name)

    @property
    def get_first_name(self):
        return self.first_name

    @property
    def get_last_name(self):
        return self.last_name

    @property
    def get_email(self):
        return self.email

    @staticmethod
    def has_perm(perm, obj=None):
        return True

    @staticmethod
    def has_module_perms(app_label):
        return True

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self
