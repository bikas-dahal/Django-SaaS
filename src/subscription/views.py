from django.shortcuts import render, redirect
from .models import SubscriptionPrice, UserSubscription
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import helpers.billing

from django.urls import reverse

@login_required
def user_subscription_view(request):
    user_sub_obj, created = UserSubscription.objects.get_or_create(user = request.user)
    
    if request.method == 'POST':
        if user_sub_obj.stripe_id:
            sub_data = helpers.billing.get_subscription(user_sub_obj.stripe_id, raw=False)
            for k, v in sub_data.items():
                setattr(user_sub_obj, k, v)
            user_sub_obj.save()
            messages.success(request, 'Your subscription has been updated.')
        return redirect(user_sub_obj.get_absolute_url())
        
    return render(request, 'subscription/user_detail_view.html', {
        'subscription': user_sub_obj,
        'username': request.user
    })

@login_required
def user_subscription_cancel_view(request):
    user_sub_obj, created = UserSubscription.objects.get_or_create(user = request.user)
    
    if request.method == 'POST':
        if user_sub_obj.stripe_id and user_sub_obj.status:
            sub_data = helpers.billing.cancel_subscription(
                user_sub_obj.stripe_id, 
                raw=False,
                feedback='other',
                cancel_at_period_end=True,
                reason='User wanted to end'
            )
            for k, v in sub_data.items():
                setattr(user_sub_obj, k, v)
            user_sub_obj.save()
            messages.success(request, 'Your subscription has been canceled.')
        return redirect(user_sub_obj.get_absolute_url())
        
    return render(request, 'subscription/user_cancel_view.html', {
        'subscription': user_sub_obj,
        'username': request.user
    })

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