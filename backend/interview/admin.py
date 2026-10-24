from django.contrib import admin
from .models import InterviewAnswer, InterviewQuestion, InterviewResult, InterviewSession

admin.site.register(InterviewSession)
admin.site.register(InterviewQuestion)
admin.site.register(InterviewAnswer)
admin.site.register(InterviewResult)