from django.shortcuts import render
from .models import PageVisit
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings 


LOGIN_URL = settings.LOGIN_URL

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

VALID_CODE = 'abc123'

@staff_member_required(login_url=LOGIN_URL)
@login_required
def pw_protected_view(request, *args, **kwargs):

    is_allowed = request.session.get('protected_page_allowed') or 0

    if request.method == 'POST':
        user_sent = request.POST.get('code') or None 
        if user_sent == VALID_CODE:
            is_allowed = 1
            request.session['protected_page_allowed'] = is_allowed
    if is_allowed:
        return render(request, "protected/view.html", {})
    return render(request, "protected/entry.html", {})
