from django.shortcuts import render
from .models import SubscriptionPrice

def subscription_price_view(request):
    qs = SubscriptionPrice.objects.filter(featured=True)
    monthly_qs = qs.filter(
        interval=SubscriptionPrice.IntervalChoices.MONTHLY
    )
    yearly_qs = qs.filter(
        interval=SubscriptionPrice.IntervalChoices.YEARLY
    )

    return render(
        request,
        'subscription/pricing.html',
        {
            'monthly_qs': monthly_qs,
            'yearly_qs': yearly_qs,
        }
    )