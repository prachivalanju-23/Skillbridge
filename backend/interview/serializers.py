from rest_framework import serializers
from .models import InterviewResult


class InterviewResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewResult
        fields = ['id', 'role', 'level', 'overall_score', 'technical',
                  'communication', 'accuracy', 'summary', 'created_at']