from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout


def unauthenticated_customer(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/customer')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def customer_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return view_func(request, *args, **kwargs)
        else:
            logout(request)
            messages.info(request, 'You are not a customer! Please sign up!')
            return redirect('/customer_login')

    return wrapper_func
