from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
import helpers.billing
from django.urls import reverse
from django.contrib import messages

from subscription.models import SubscriptionPrice, Subscription, UserSubscription
from django.contrib.auth import get_user_model
from django.conf import settings 

BASE_URL = settings.BASE_URL
User = get_user_model()

def product_price_redirect_view(request, price_id = None, *args, **kwargs):
    request.session['checkout_subscription_price_id'] = price_id
    print(request)
    # print('abc')
    url =  reverse('checkouts:checkout_start')
    print(url)
    return redirect(url)

@login_required
def checkout_redirect_view(request):
    checkout_subscription_price_id = request.session.get('checkout_subscription_price_id', None)
    print(f'cspi:{checkout_subscription_price_id}')
    if checkout_subscription_price_id is None:
        return redirect('subscription:pricing')
    customer_stripe_id = request.user.customer.stripe_id
    print(f'csid = {customer_stripe_id}')
    try:
        obj = SubscriptionPrice.objects.get(id = checkout_subscription_price_id)
    except:
        
        obj = None

    print(obj)

    if obj is None:
        return redirect('subscription:pricing')
    
    success_url_path = reverse('checkouts:checkout_end')
    pricing_url_path = reverse('subscription:pricing')

    price_stripe_id = obj.stripe_id

    
    success_url = f"{BASE_URL}{success_url_path}"
    cancel_url = f"{BASE_URL}{pricing_url_path}"

    url = helpers.billing.start_checkout_session(
        success_url = success_url,
        customer_id = customer_stripe_id,
        price_stripe_id = price_stripe_id,
        cancel_url=cancel_url,
        raw= False

    )

    # print(customer_stripe_id)
    return redirect(url)



def checkout_final_view(request):
    session_id = request.GET.get('session_id')
    checkout_data = helpers.billing.get_checkout_customer_plan(session_id)

    plan_id = checkout_data.pop('plan_id')
    customer_id = checkout_data.pop('customer_id')
    sub_stripe_id = checkout_data.pop('sub_stripe_id')
    subscription_data = {**checkout_data}

    try:
        sub_obj = Subscription.objects.get(subscriptionprice__stripe_id = plan_id)
    except:
        sub_obj = None
    try:
        user_obj = User.objects.get(customer__stripe_id = customer_id)
    except:
        sub_obj = None

    _user_sub_exists = False
    updated_sub_options = {
        'subscription': sub_obj,
        'stripe_id': sub_stripe_id,
        'user_cancelled': False,
        **subscription_data
    }

    try:
        _user_sub_obj = UserSubscription.objects.get(user=user_obj)
        _user_sub_exists = True
    except UserSubscription.DoesNotExist:
        _user_sub_obj = UserSubscription.objects.create(
            user = user_obj,
            **updated_sub_options
        )
    except:
        _user_sub_obj = None

    print(sub_obj, user_obj, _user_sub_obj)

    if None in [sub_obj, user_obj, _user_sub_obj]:
        return HttpResponseBadRequest("Error with your account, contact for further  ")


    if _user_sub_exists:
        # cancel old sub
        old_stripe_id = _user_sub_obj.stripe_id
        same_stripe_id = sub_stripe_id == old_stripe_id

        if old_stripe_id is not None and not same_stripe_id:
            try:
                helpers.billing.cancel_subscription(
                    old_stripe_id,
                    reason="Auto ended, new membership",
                    feedback='other'
                )
            except:
                pass

        # assign new sub
        for k, v in updated_sub_options.items():
            setattr(_user_sub_obj, k, v)
        _user_sub_obj.save()
        messages.success(request, 'Success! Thank you for joining.')
        return redirect(_user_sub_obj.get_absolute_url())
    return render(
        request,
        'checkouts/success.html',

    )
