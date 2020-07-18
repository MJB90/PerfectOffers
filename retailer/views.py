from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateRetailUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, retail_only
# from bokeh.plotting import figure
# from bokeh.embed import components
# from bokeh.models import HoverTool, LassoSelectTool, WheelZoomTool, PointDrawTool, ColumnDataSource

# from bokeh.palettes import Category20c, Spectral6
# from bokeh.transform import cumsum
# from numpy import pi
# from bokeh.resources import CDN
# Create your views here.


@login_required(login_url='/login')
@retail_only
def home(request):
    context = {}
    return render(request, "retail_home.html", context)


@login_required(login_url='/login')
@retail_only
def dashboard(request):
    # lang = ['H&M', 'ZARA', 'Levis', 'Pepe Jeans', 'Max', 'HRX']
    # counts = [25, 30, 8, 22, 12, 17]

    # p = figure(x_range=lang, plot_height=450, title="Clothing Brands Popularity",
    #            toolbar_location="below", tools="pan,wheel_zoom,box_zoom,reset, hover, tap, crosshair")

    # source = ColumnDataSource(
    #     data=dict(lang=lang, counts=counts, color=Spectral6))
    # p.add_tools(LassoSelectTool())
    # p.add_tools(WheelZoomTool())

    # p.vbar(x='lang', top='counts', width=.8,
    #        color='color', legend="lang", source=source)
    # p.legend.orientation = "horizontal"
    # p.legend.location = "top_center"

    # p.xgrid.grid_line_color = "black"
    # p.y_range.start = 0
    # p.line(x=lang, y=counts, color="black", line_width=2)

    # script, div = components(p)

    context = {}
    return render(request, "retail_dashboard.html", context)


@login_required(login_url='/login')
@retail_only
def orders(request):
    context = {}
    return render(request, "retail_orders.html", context)


@login_required(login_url='/login')
@retail_only
def subscription(request):
    context = {}
    return render(request, "retail_subscription.html", context)


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
