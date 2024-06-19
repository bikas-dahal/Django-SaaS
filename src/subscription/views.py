from django.shortcuts import render
from .models import SubscriptionPrice

from django.urls import reverse

def subscription_price_view(request, interval='year'):
    qs = SubscriptionPrice.objects.filter(featured=True)
    inv_mo = SubscriptionPrice.IntervalChoices.MONTHLY
    inv_yr = SubscriptionPrice.IntervalChoices.YEARLY
    print(inv_yr)
    
    object_list = qs.filter(
        interval=inv_mo
    )

    url_path_name = "subscription:pricing_interval"
    mo_url = reverse(url_path_name, kwargs={'interval': inv_mo})
    yo_url = reverse(url_path_name, kwargs={'interval': inv_yr})
    # print(mo_url)
    print(yo_url)
    active = inv_mo
    print(interval)

    if interval == inv_yr:
        active = inv_yr
        object_list = qs.filter(
            interval=inv_yr
        )
    return render(
        request,
        'subscription/pricing.html',
        {
            'object_list': object_list,
            'mo_url': mo_url,
            'yo_url': yo_url,
            'active': active
        }
    )