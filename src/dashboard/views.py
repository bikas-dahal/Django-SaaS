from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard_view(request):
    return render(
        request,
        'dashboard/main.html',
        {}
    )