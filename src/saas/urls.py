
from django.contrib import admin
from django.urls import path,include

from auth.views import login_view, register_view

from landing import views as landing_views

urlpatterns = [
    path('', landing_views.landing_page_view, name='landing'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('visits.urls', namespace='visits')),
    path('checkout/', include('checkouts.urls', namespace='checkouts')),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('subscription/', include('subscription.urls', namespace='subscription')),
]
