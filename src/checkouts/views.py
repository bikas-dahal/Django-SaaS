from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
import helpers.billing
from django.urls import reverse

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

    customer_id, plan_id = helpers.billing.get_checkout_customer_plan(session_id)
    # print(price_qs)

    try:
        sub_obj = Subscription.objects.get(subscriptionprice__stripe_id = plan_id)
    except:
        sub_obj = None

    try:
        user_obj = User.objects.get(customer__stripe_id = customer_id)
    except:
        sub_obj = None

    _user_sub_exists = False
    try:
        _user_sub_obj = UserSubscription.objects.get(user=user_obj)
        _user_sub_exists = True

    except UserSubscription.DoesNotExist:
        _user_sub_obj = UserSubscription.objects.create(
            user = user_obj,
            subscription = sub_obj
        )
    
    except:
        _user_sub_obj = None

    if None in [sub_obj, user_obj, _user_sub_obj]:
        return HttpResponseBadRequest("Error with your account, contact for further  ")


    if _user_sub_exists:
        _user_sub_obj.subscription = sub_obj
        _user_sub_obj.save()

    return render(
        request,
        'checkouts/success.html',

    )
