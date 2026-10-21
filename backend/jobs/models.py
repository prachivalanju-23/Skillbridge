from django.db import models

from core.models import Skill


class Job(models.Model):
    title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=100, default='Remote')
    job_type = models.CharField(max_length=30, default='Full-time')
    level = models.CharField(max_length=30, default='Beginner')
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    apply_link = models.URLField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} at {self.company}'


class JobSkill(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='job_skills')

    class Meta:
        ordering = ['id']
        unique_together = ('job', 'skill')

    def __str__(self):
        return f'{self.job.title}: {self.skill.name}'