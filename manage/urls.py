from django.urls import path
from . import views


urlpatterns = [
    path('/', views.startTest.as_view()),
    path('/action/',views.startProblem.as_view()),

]
