from django.urls import path
from .views import home

app_name = 'retailer'

urlpatterns = [
    path('retailer/', home, name="home"),
]
