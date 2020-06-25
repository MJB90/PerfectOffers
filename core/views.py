from django.shortcuts import render
from .models import Item

# Create your views here.


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


def checkout(request):
    return render(request, "checkout.html")


def notifications(request):
    return render(request, "notifications.html")


def home(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "home.html", context)
