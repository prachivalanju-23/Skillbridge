from django.urls import path
from . import views

urlpatterns = [
    path('', views.career_list),
    path('<int:pk>/', views.career_detail),
]