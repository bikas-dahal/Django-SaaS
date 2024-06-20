
from django.contrib import admin
from django.urls import path,include

from auth.views import login_view, register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('visits.urls', namespace='visits')),
    path('checkout/', include('checkouts.urls', namespace='checkouts')),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('subscription/', include('subscription.urls', namespace='subscription')),
]
