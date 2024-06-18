from typing import Iterable
from django.db import models
from django.conf import settings 
import helpers.billing

from allauth.account.signals import (
    email_confirmed as allauth_email_confirmed,
    user_signed_up as allauth_user_signed_up
)

User = settings.AUTH_USER_MODEL

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=50, blank=True, null=True)
    init_email = models.EmailField(blank=True, null=True)
    init_email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        name = self.user.username
        if not self.stripe_id:
            if self.init_email_confirmed and self.init_email:
                email = self.user.email 
                self.stripe_id = helpers.billing.create_customer(name, email,
                metadata = {
                    'user': self.user.username,
                    'email': self.user.email
                }
                )

        super().save(*args, **kwargs)


def user_signed_up(request, user, **kwargs):
    email = user.email 
    Customer.objects.create(
        user=user, 
        init_email=email, 
        init_email_confirmed=False
    ) 
    
allauth_user_signed_up.connect(user_signed_up)

def email_confirmed(request, email_address, **kwargs):
    qs = Customer.objects.filter(
        init_email=email_address.email,
        init_email_confirmed = False
    )

    for obj in qs:
        obj.init_email_confirmed = True
        obj.save()

allauth_email_confirmed.connect(email_confirmed)