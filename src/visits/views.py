from django.shortcuts import render
from .models import PageVisit

# Create your views here.


def index(request):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path=request.path)
    try:
        percent = (page_qs.count() * 100.0) / qs.count()
    except:
        percent = 0
    my_title = "My Page"
    my_context = {
        "page_title": my_title,
        "page_visit_count": page_qs.count(),
        "percent": percent,
        "total_visit_count": qs.count(),
    }
    PageVisit.objects.create(path=request.path)
    

    return render(request, 'index.html', my_context)


def visits(request):
    visits = PageVisit.objects.all()
    return render(request, 'visits.html', {'visits': visits})

