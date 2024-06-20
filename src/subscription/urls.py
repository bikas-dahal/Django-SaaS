from django.urls import path 
from . import views

app_name = 'subscription'

urlpatterns = [
    path('pricing/', views.subscription_price_view, name='pricing'),
    path('pricing/<str:interval>/', views.subscription_price_view, name='pricing_interval'),
    path('user/', views.user_subscription_view, name='user_subscription'),
    path('user/cancel/', views.user_subscription_cancel_view, name='user_subscription_cancel'),
]