from django.urls import path 
from . import views

app_name = 'subscrition'

urlpatterns = [
    path('pricing/', views.subscription_price_view, name='pricing')
]