from django.conf import settings
from django.db import models
from core.models import Skill, Career

User = settings.AUTH_USER_MODEL


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, blank=True)
    email = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    education = models.JSONField(default=list)
    projects = models.JSONField(default=list)
    certifications = models.JSONField(default=list)
    experience = models.JSONField(default=list)
    resume_score = models.IntegerField(default=0)


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    raw_text = models.TextField()
    score = models.IntegerField(default=0)
    score_breakdown = models.JSONField(default=dict)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class StudentSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'skill')


class SkillGap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    career = models.ForeignKey(Career, on_delete=models.CASCADE)
    matched = models.JSONField(default=list)
    missing = models.JSONField(default=list)
    percentage = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'career')