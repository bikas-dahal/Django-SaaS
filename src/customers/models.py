from typing import Iterable
from django.db import models
from django.conf import settings 
import helpers.billing

User = settings.AUTH_USER_MODEL

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        email = self.user.email 
        name = self.user.username
        if not self.stripe_id:
            self.stripe_id = helpers.billing.create_customer(name, email)

        super().save(*args, **kwargs)

