from django.urls import path
from . import views

urlpatterns = [
    path('goal/', views.career_goal),
    path('career/<int:career_id>/', views.roadmap_for_career),
]