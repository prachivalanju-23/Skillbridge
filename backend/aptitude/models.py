from django.conf import settings
from django.db import models

CATEGORIES = ['Logical', 'Quantitative', 'Verbal', 'Technical']


class Question(models.Model):
    category = models.CharField(max_length=20, choices=[(c, c) for c in CATEGORIES])
    text = models.CharField(max_length=500)
    options = models.JSONField()  # list of 4 strings
    correct_index = models.PositiveSmallIntegerField()
    explanation = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f'[{self.category}] {self.text[:60]}'


class AptitudeTest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='aptitude_tests')
    created_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    test = models.ForeignKey(AptitudeTest, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_index = models.PositiveSmallIntegerField()
    is_correct = models.BooleanField()


class TestResult(models.Model):
    test = models.OneToOneField(AptitudeTest, on_delete=models.CASCADE, related_name='result')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='aptitude_results')
    score = models.PositiveSmallIntegerField()
    total = models.PositiveSmallIntegerField()
    category_scores = models.JSONField(default=list)  # [{category, correct, total, percentage}]
    created_at = models.DateTimeField(auto_now_add=True)