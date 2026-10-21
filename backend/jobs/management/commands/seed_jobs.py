from django.core.management.base import BaseCommand

from core.models import Skill
from jobs.models import Job, JobSkill

# title, company, location, type, level, category, description, skills
JOBS = [
    ('Junior React Developer', 'BrightApps Technologies', 'Pune', 'Full-time', 'Beginner', 'Frontend Developer',
     'Build responsive user interfaces using React and work with REST APIs.',
     ['React', 'JavaScript', 'HTML', 'CSS', 'Git']),
    ('Frontend Developer', 'PixelCraft Solutions', 'Bengaluru', 'Full-time', 'Intermediate', 'Frontend Developer',
     'Develop and maintain web apps with a focus on performance and UI quality.',
     ['React', 'JavaScript', 'HTML', 'CSS', 'Tailwind CSS', 'Testing']),
    ('Full Stack Developer Intern', 'CodeNest Labs', 'Remote', 'Internship', 'Beginner', 'Full Stack Developer',
     'Work on both frontend and backend features of a MERN stack product.',
     ['React', 'Node.js', 'Express.js', 'MongoDB', 'JavaScript']),
    ('Full Stack Developer', 'StackWorks India', 'Mumbai', 'Full-time', 'Intermediate', 'Full Stack Developer',
     'Design APIs, build UI screens and manage databases for web applications.',
     ['React', 'Node.js', 'Express.js', 'MongoDB', 'Git', 'REST API']),
    ('Backend Developer', 'ServerLogic Pvt Ltd', 'Hyderabad', 'Full-time', 'Intermediate', 'Backend Developer',
     'Build secure and scalable APIs and manage database operations.',
     ['Node.js', 'Express.js', 'MongoDB', 'JWT', 'REST API']),
    ('Data Analyst Trainee', 'InsightEdge Analytics', 'Pune', 'Full-time', 'Beginner', 'Data Analyst',
     'Clean data, create reports and build dashboards for business teams.',
     ['Python', 'SQL', 'Excel', 'Data Visualization', 'Statistics']),
    ('Junior AI/ML Engineer', 'NeuralPath AI', 'Remote', 'Full-time', 'Beginner', 'AI/ML Engineer',
     'Train and test machine learning models and prepare datasets.',
     ['Python', 'Machine Learning', 'Pandas', 'NumPy', 'Scikit-learn']),
    ('Python Backend Intern', 'DataBridge Systems', 'Remote', 'Internship', 'Beginner', 'Backend Developer',
     'Assist in building Python APIs and database integrations.',
     ['Python', 'SQL', 'REST API', 'Git']),
]


class Command(BaseCommand):
    help = 'Load sample jobs'

    def handle(self, *args, **options):
        Job.objects.all().delete()

        for title, company, location, job_type, level, category, desc, skill_names in JOBS:
            job = Job.objects.create(
                title=title,
                company=company,
                location=location,
                job_type=job_type,
                level=level,
                category=category,
                description=desc,
            )
            for name in skill_names:
                skill, _ = Skill.objects.get_or_create(name=name)
                JobSkill.objects.create(job=job, skill=skill)

        self.stdout.write(self.style.SUCCESS(f'Loaded {len(JOBS)} jobs'))