from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.


@login_required
def profile_list_view(request, username = None, *args, **kwargs):
    user = request.user 
    users = User.objects.all()
    context = {
        'object_list': users
    }
    return render(request, 'profiles/list.html', context)





@login_required
def profile_view(request, username=None, *args, **kwargs):
    user = request.user
    profile_user_obj = get_object_or_404(
        User, username=user.username
    )
    print(profile_user_obj)

    print(
        user.has_perm('subscription.basic'),
        user.has_perm('subscription.pro'),
        user.has_perm('subscription.advancedd'),
    )


    user_groups = user.groups.all()
    print(user_groups)

    # if user_groups.filter(name__icontains='view').exists():
    #     return HttpResponse('Les go')

    is_me = profile_user_obj == user

    context = {
        'object': profile_user_obj,
        'instance': profile_user_obj,
        'owner': is_me

    }

    username = username
    # print(username)

    # username = kwargs.get('username')
    context = {
        'username': username
    }
    # profile_user_obj = User.objects.get(username=username)
    # print(profile_user_obj)
    return render(request, 'profiles/profile.html', context)

