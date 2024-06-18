from django.contrib import admin
from .models import Subscription, UserSubscription, SubscriptionPrice

class SubscriptionPrice(admin.StackedInline):
    model = SubscriptionPrice
    can_delete =False
    readonly_fields = ['stripe_id']
    extra = 0


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'active')
    inlines = [SubscriptionPrice]
    readonly_fields = ['stripe_id']



admin.site.register(Subscription, SubscriptionAdmin)

admin.site.register(UserSubscription)