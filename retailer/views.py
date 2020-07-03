from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateRetailUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, retail_only
# Create your views here.


@login_required(login_url='/login')
@retail_only
def home(request):
    context = {}
    return render(request, "retail_home.html", context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/retailer')
        else:
            messages.info(request, 'Username or password is incorrect')
    context = {}
    return render(request, "retail_login.html", context)


def logoutPage(request):
    logout(request)
    return redirect('/login')


@unauthenticated_user
def registerPage(request):
    form = CreateRetailUserForm()

    if request.method == 'POST':
        form = CreateRetailUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='retailer')
            user.groups.add(group)

            messages.success(request, 'Account is created for ' + username)
            return redirect('/login')

    context = {'form': form}
    return render(request, "retail_register.html", context)


def planPage(request):
    context = {}
    return render(request, "retail_pricing.html", context)
