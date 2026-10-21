from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/interview/', include('interview.urls')),
    path('api/aptitude/', include('aptitude.urls')),
    path('api/progress/', include('progress.urls')),
]