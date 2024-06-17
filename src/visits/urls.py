from django.urls import path
from . import views

app_name = "views"

urlpatterns = [
    path("", views.index, name="home"),
    path("visits/", views.visits, name="visits"),
    path("protected/", views.pw_protected_view, name="protected"),
]
