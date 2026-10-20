from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/careers/', include('roadmap.career_urls')),
    path('api/roadmap/', include('roadmap.urls')),
    path('api/jobs/', include('jobs.urls')),
    # each member adds only their own line below, for example:
    # path('api/resume/', include('resume.urls')),
]