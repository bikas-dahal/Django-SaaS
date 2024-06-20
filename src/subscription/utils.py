from typing import Any
from django.core.management.base import BaseCommand 

import helpers.billing

from customers.models import Customer
from subscription.models import Subscription, UserSubscription
    
def clear_dangling_subs(self, *args: Any, **options: Any) -> str | None:
    qs = Customer.objects.filter(stripe_id__isnull=False)

    for obj in qs:
        user = obj.user 
        customer_stripe_id = obj.stripe_id
        print(f'Sync {user} - {customer_stripe_id} subs and remove old ones')
        subs = helpers.billing.get_customer_active_subscriptions(customer_stripe_id)
        for sub in subs:
            existing_user_subs_qs= UserSubscription.objects.filter(
                stripe_id__iexact= f'{sub.id}'.strip()
            )
            if existing_user_subs_qs.exists():
                continue
            helpers.billing.cancel_subscription(
                sub.id,
                reason='Dangling active subscription',
                cancel_at_period_end=False
            )
            # print(sub.id, existing_user_subs_qs.exists())

def sync_subs_group_permissions():  
    qs = Subscription.objects.filter(active=True)
    for obj in qs:
        sub_perm = obj.groups.all()
        for group in obj.groups.all():
            group.permissions.set(sub_perm)