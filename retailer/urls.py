from django.urls import path
from .views import home, loginPage, logoutPage, registerPage

app_name = 'retailer'

urlpatterns = [
    path('retailer/', home, name="home"),
    path('login/', loginPage, name="login"),
    path('logout/', logoutPage, name="logout"),
    path('register/', registerPage, name="register")
]
