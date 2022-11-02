from django.urls import path
from . import views


urlpatterns = [
    path('', views.getCustomers.as_view()),
]
