from django.urls import path
from .views import home, loginPage, logoutPage, registerPage, planPage, dashboard, subscription, orders

app_name = 'retailer'

urlpatterns = [
    path('retailer/', home, name="home"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutPage, name="logout"),
    path('register/', registerPage, name="register"),
    path('plan/', planPage, name="plan"),
    path('dashboard/', dashboard, name="dashboard"),
    path('subscription/', subscription, name="subscription"),
    path('retail_orders/', orders, name="retail_orders")
]
