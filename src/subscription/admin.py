from django.contrib import admin
from .models import Subscription, UserSubscription



admin.site.register(Subscription)

admin.site.register(UserSubscription)