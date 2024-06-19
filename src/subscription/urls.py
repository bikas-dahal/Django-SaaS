from django.urls import path 
from . import views

app_name = 'subscription'

urlpatterns = [
    path('pricing/', views.subscription_price_view, name='pricing'),
    path('pricing/<str:interval>/', views.subscription_price_view, name='pricing_interval')
]