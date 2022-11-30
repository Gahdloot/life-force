from django.test import TestCase

# Create your tests here.


from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        ANON = "ANON", "Anon"
        CLIENT = "CLIENT", "Client"
        ORGANIZATION = "ORGANIZATION", "Organization"

    base_role = Role.ANON

    role = models.CharField(max_length=50, choices=Role.choices)

    email = models.EmailField(unique=True, max_length=255, verbose_name='email address')
    username = models.CharField(max_length=50, default='Anon', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.email
#dont forget to add the str method just incase you encounter an error because str is supposed to return username


class Client(User):
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=250, null=True, blank=True)
    nin = models.IntegerField(null=True)
    age = models.IntegerField(default=19, null=True)
    weight = models.IntegerField(default=130, null=True)
    blood_group = models.CharField(max_length=4, null=True)
    wants_to_donate = models.BooleanField(default=True)
    needs_donation = models.BooleanField(default=False)
    base_role = User.Role.CLIENT

    #learn 1 to 1 rel

    # class Meta:
    #     proxy = True

class Organization(User):
    company_name = models.CharField(max_length=250)
    CAC = models.CharField(max_length=30)
    location = models.CharField(max_length=250)
    address = models.TextField(null=True, blank=True)
    base_role = User.Role.ORGANIZATION

    #learn 1 to 1 rel

    # class Meta:
    #     proxy = True


class Transaction():
    #two users, date time, isapproved[]
    #holds two users, patient and donors
    #hold organisation
    #successful


    # temp
    hospital = models.ForeignKey(Organization, on_delete=models.SET_NULL)
    clients = models.ForeignKey(Client, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    pass

#class Patient():
    #one to many relationship # hospital and patients
    #pass



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
