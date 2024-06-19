from django.urls import path 
from . import views

app_name = 'checkouts'

urlpatterns = [
    path('sub-price/<int:price_id>/', 
         views.product_price_redirect_view, 
         name='sub_price_checkout'
        ),
    path('start/', 
         views.checkout_redirect_view, 
         name='checkout_start'
        ),
    path('checkout/success/', 
         views.checkout_final_view, 
         name='checkout_end'
        ),
    

]