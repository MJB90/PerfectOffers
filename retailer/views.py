from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateRetailUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='/login')
def home(request):
    context = {}
    return render(request, "retail_home.html", context)


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


def registerPage(request):
    form = CreateRetailUserForm()

    if request.method == 'POST':
        form = CreateRetailUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account is created for ' + user)
            return redirect('/login')

    context = {'form': form}
    return render(request, "retail_register.html", context)
