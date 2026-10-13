from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Career(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    required_skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.title