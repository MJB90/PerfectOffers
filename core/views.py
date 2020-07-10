from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Order, OrderItem
from .forms import CreateCustomerForm
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import unauthenticated_customer, customer_only
from django.utils.decorators import method_decorator
# Create your views here.


@login_required(login_url='/customer_login')
def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


@login_required(login_url='/customer_login')
def checkout(request):
    return render(request, "checkout.html")


@login_required(login_url='/customer_login')
def notifications(request):
    return render(request, "notifications.html")


@method_decorator(customer_only, name='dispatch')
class HomeView(LoginRequiredMixin, ListView):
    login_url = '/customer_login'
    model = Item
    template_name = "home.html"


@method_decorator(customer_only, name='dispatch')
class OrderSummaryView(LoginRequiredMixin, View):
    login_url = '/customer_login'

    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")


@method_decorator(customer_only, name='dispatch')
class ItemDetailView(LoginRequiredMixin, DetailView):
    login_url = '/customer_login'
    model = Item
    template_name = "product.html"


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity is updated")
        else:
            messages.info(request, "This item is added to cart")
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item is added to cart")

    return redirect("core:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item, created = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
        messages.info(request, "This item is removed from cart")
    return redirect("core:product", slug=slug)


def CloginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/customer')
        else:
            messages.info(request, 'Username or password is incorrect')
    context = {}
    return render(request, "customer_login.html", context)


def ClogoutPage(request):
    logout(request)
    return redirect('/customer_login')


def CregisterPage(request):
    form = CreateCustomerForm()

    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'Account is created for ' + username)
            return redirect('/customer_login')

    context = {'form': form}
    return render(request, "customer_register.html", context)
