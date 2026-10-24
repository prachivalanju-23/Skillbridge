from django.core.management.base import BaseCommand
from core.models import Skill, Career

ROLES = {
    'Full Stack Developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Node.js', 'Express.js', 'MongoDB', 'Git'],
    'Frontend Developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Git', 'Responsive Design'],
    'Data Analyst': ['Python', 'SQL', 'Excel', 'Data Visualization', 'Statistics', 'Pandas'],
    'AI/ML Engineer': ['Python', 'Machine Learning', 'Pandas', 'NumPy', 'Scikit-learn'],
}


class Command(BaseCommand):
    help = 'Add test careers (safe to run many times)'

    def handle(self, *args, **options):
        for title, skills in ROLES.items():
            career, _ = Career.objects.get_or_create(title=title)
            for name in skills:
                skill, _ = Skill.objects.get_or_create(name=name)
                career.required_skills.add(skill)
        self.stdout.write('Test careers added')