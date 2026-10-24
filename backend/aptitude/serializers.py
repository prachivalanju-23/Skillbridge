from rest_framework import serializers
from .models import Question, TestResult


class QuestionPublicSerializer(serializers.ModelSerializer):
    """No correct_index or explanation, so answers never reach the browser."""
    class Meta:
        model = Question
        fields = ['id', 'category', 'text', 'options']


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ['id', 'score', 'total', 'category_scores', 'created_at']