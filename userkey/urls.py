from django.urls import path
from . import views


urlpatterns = [
    path('', views.startTest.as_view()),
    path('problems/', views.startProblem.as_view()),

]
