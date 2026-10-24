from django.conf import settings
from django.db import models


class InterviewSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interview_sessions')
    role = models.CharField(max_length=100)
    level = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='in-progress')
    total_questions = models.PositiveSmallIntegerField(default=5)
    current_difficulty = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)


class InterviewQuestion(models.Model):
    session = models.ForeignKey(InterviewSession, on_delete=models.CASCADE, related_name='questions')
    order = models.PositiveSmallIntegerField()
    text = models.CharField(max_length=500)
    difficulty = models.PositiveSmallIntegerField()
    keywords = models.JSONField(default=list)  # used by the evaluator, never sent to the browser

    class Meta:
        ordering = ['order']


class InterviewAnswer(models.Model):
    question = models.OneToOneField(InterviewQuestion, on_delete=models.CASCADE, related_name='answer')
    answer_text = models.TextField()
    score = models.PositiveSmallIntegerField()
    technical = models.PositiveSmallIntegerField()
    communication = models.PositiveSmallIntegerField()
    accuracy = models.PositiveSmallIntegerField()
    feedback = models.CharField(max_length=500)


class InterviewResult(models.Model):
    session = models.OneToOneField(InterviewSession, on_delete=models.CASCADE, related_name='result')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interview_results')
    role = models.CharField(max_length=100)
    level = models.CharField(max_length=20)
    overall_score = models.FloatField()
    technical = models.FloatField()
    communication = models.FloatField()
    accuracy = models.FloatField()
    summary = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)