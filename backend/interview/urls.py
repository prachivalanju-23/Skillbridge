from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.start),
    path('answer/', views.answer),
    path('result/<int:pk>/', views.result),
    path('history/', views.history),
]