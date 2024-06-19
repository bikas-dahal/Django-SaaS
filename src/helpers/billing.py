import stripe 
from decouple import config 

DJANGO_DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)

STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='', cast=str)


if 'sk_test' in STRIPE_SECRET_KEY and not DJANGO_DEBUG:
    raise ValueError("Stripe secret key is in test mode.")


stripe.api_key = STRIPE_SECRET_KEY


def create_customer(
        name = '',
        email = '',
        metadata={},
        raw=False
    ):
    response = stripe.Customer.create(
        name=name,
        email=email,
        metadata = metadata,
    )
    if raw:
        return response
    stripe_id = response.id 
    return stripe_id 

def create_product(
        name = '',
        metadata = {},
        raw=False
    ):
    response = stripe.Product.create(
        name=name,
        metadata=metadata
    )
    if raw:
        return response
    stripe_id = response.id 
    return stripe_id


def create_price(
        currency = 'usd',
        unit_amount = '9999',
        product = None,
        interval ='month',
        metadata = {},
        raw=False
    ):
    if product is None:
        return None 
    response = stripe.Price.create(
        currency = currency,
        unit_amount = unit_amount,
        recurring = {
            'interval': interval
        },
        product = product,
        metadata = metadata
    )
    if raw:
        return response
    stripe_id = response.id 
    return stripe_id

def start_checkout_session(
        success_url = '', 
        raw=True,
        price_stripe_id = '',
        cancel_url = '',
        customer_id = ''
    ):

    if not success_url.endswith('?session_id={CHECKOUT_SESSION_ID}'):
        success_url += '?session_id={CHECKOUT_SESSION_ID}'

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': price_stripe_id,
                'quantity': 1,
            },
        ],
        mode='subscription',
        success_url=success_url,
        cancel_url= cancel_url,
        customer=customer_id
    )

    if raw:
        return session
    return session.url

def get_checkout_session(stripe_id, raw=True):

    response = stripe.checkout.Session.retrieve(
        stripe_id,
    )


    if raw:
        return response
    return response.url

def get_subscription(stripe_id, raw=True):

    response = stripe.Subscription.retrieve(
        stripe_id,
    )


    if raw:
        return response
    return response.url

def get_checkout_customer_plan(session_id):
    checkout_r = get_checkout_session(session_id, raw=True)
    customer_id = checkout_r.customer
    sub_stripe_id = checkout_r.subscription
    subscription_r = get_subscription(sub_stripe_id, raw=True)
    sub_plan = subscription_r.plan
    return customer_id, sub_plan.id