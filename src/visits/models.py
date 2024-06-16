from django.db import models

# Create your models here.

class PageVisit(models.Model):
    path = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)