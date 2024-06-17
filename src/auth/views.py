from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login 

from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm


User = get_user_model()

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'auth/login.html')
    return render(request, 'auth/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # username_exist = User.objects.filter(
        #     username__iexact=username,
        # ).exists()
        # email_exist = User.objects.filter(
        #     email__iexact=email,
        # ).exists()



        user = User.objects.create_user(username=username, email=email, password=password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'auth/register.html')
    return render(request, 'auth/register.html')
