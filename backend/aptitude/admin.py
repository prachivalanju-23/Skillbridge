from django.contrib import admin
from .models import Answer, AptitudeTest, Question, TestResult

admin.site.register(Question)
admin.site.register(AptitudeTest)
admin.site.register(Answer)
admin.site.register(TestResult)