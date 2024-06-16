from django.shortcuts import render
from .models import PageVisit

# Create your views here.


def index(request):

    qs = PageVisit.objects.all()
    

    return render(request, 'index.html')


def visits(request):
    visits = PageVisit.objects.all()
    return render(request, 'visits.html', {'visits': visits})

