from django.contrib import admin
from .models import StudentProfile, Resume, StudentSkill, SkillGap

admin.site.register(StudentProfile)
admin.site.register(Resume)
admin.site.register(StudentSkill)
admin.site.register(SkillGap)