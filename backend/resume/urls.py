from django.urls import path
from .views import ResumeUploadView, ProfileView, RolesView, SkillGapView

urlpatterns = [
    path('upload/', ResumeUploadView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('roles/', RolesView.as_view()),
    path('skill-gap/', SkillGapView.as_view()),
]