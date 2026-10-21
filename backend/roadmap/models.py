from django.conf import settings
from django.db import models

from core.models import Career


class CareerGoal(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='career_goal'
    )
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='goals')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} -> {self.career.title}'


class RoadmapStep(models.Model):
    career = models.ForeignKey(
        Career, on_delete=models.CASCADE, related_name='roadmap_steps'
    )
    order = models.PositiveIntegerField()
    skill = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    weeks = models.PositiveIntegerField(default=2)
    resource_title = models.CharField(max_length=150, blank=True)
    resource_url = models.URLField(max_length=300, blank=True)

    class Meta:
        ordering = ['career', 'order']
        unique_together = ('career', 'order')

    def __str__(self):
        return f'{self.career.title} #{self.order} {self.skill}'