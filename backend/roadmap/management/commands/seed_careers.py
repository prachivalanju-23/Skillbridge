from django.core.management.base import BaseCommand

from core.models import Career, Skill
from roadmap.models import RoadmapStep

# weeks, description, learning link title, learning link url
LIBRARY = {
    'HTML': (1, 'Learn page structure: headings, forms, tables and semantic tags.', 'MDN HTML guide', 'https://developer.mozilla.org/en-US/docs/Web/HTML'),
    'CSS': (2, 'Style pages with selectors, flexbox, grid and responsive design.', 'MDN CSS guide', 'https://developer.mozilla.org/en-US/docs/Web/CSS'),
    'JavaScript': (4, 'Variables, functions, arrays, DOM, async code and ES6 features.', 'MDN JavaScript guide', 'https://developer.mozilla.org/en-US/docs/Web/JavaScript'),
    'Git': (1, 'Track your code with commits, branches and pull requests on GitHub.', 'Git documentation', 'https://git-scm.com/doc'),
    'React': (4, 'Build UIs with components, props, state, hooks and routing.', 'React official tutorial', 'https://react.dev/learn'),
    'Tailwind CSS': (1, 'Style quickly with utility classes and build responsive layouts.', 'Tailwind CSS docs', 'https://tailwindcss.com/docs'),
    'Testing': (2, 'Write unit tests for your code and components with Jest.', 'Jest getting started', 'https://jestjs.io/docs/getting-started'),
    'Node.js': (3, 'Run JavaScript on the server, work with modules, files and npm.', 'Node.js learn', 'https://nodejs.org/en/learn'),
    'Express.js': (2, 'Create servers, routes and middleware for your APIs.', 'Express.js guide', 'https://expressjs.com/'),
    'MongoDB': (2, 'Store data in collections, query it and model it with Mongoose.', 'MongoDB University', 'https://learn.mongodb.com/'),
    'REST API': (1, 'Design clean endpoints, use HTTP methods and return correct status codes.', 'REST API tutorial', 'https://restfulapi.net/'),
    'JWT': (1, 'Secure your APIs with token-based login and protected routes.', 'JWT introduction', 'https://jwt.io/introduction'),
    'SQL': (3, 'Query relational data with SELECT, JOIN, GROUP BY and subqueries.', 'SQL tutorial', 'https://www.w3schools.com/sql/'),
    'Python': (4, 'Learn syntax, data structures, functions and file handling.', 'Python tutorial', 'https://docs.python.org/3/tutorial/'),
    'Excel': (2, 'Use formulas, pivot tables and charts to analyse data.', 'Microsoft Excel help', 'https://support.microsoft.com/excel'),
    'Pandas': (2, 'Clean, filter and summarise tables of data in Python.', 'Pandas getting started', 'https://pandas.pydata.org/docs/getting_started/index.html'),
    'NumPy': (1, 'Work with arrays and fast numerical operations.', 'NumPy for beginners', 'https://numpy.org/doc/stable/user/absolute_beginners.html'),
    'Statistics': (3, 'Mean, variance, probability, distributions and hypothesis tests.', 'Khan Academy statistics', 'https://www.khanacademy.org/math/statistics-probability'),
    'Data Visualization': (2, 'Turn data into clear charts and dashboards.', 'Matplotlib tutorials', 'https://matplotlib.org/stable/tutorials/index.html'),
    'Machine Learning': (4, 'Train and evaluate models for prediction and classification.', 'Kaggle: Intro to ML', 'https://www.kaggle.com/learn/intro-to-machine-learning'),
    'Scikit-learn': (2, 'Build ML pipelines with ready-made algorithms.', 'Scikit-learn getting started', 'https://scikit-learn.org/stable/getting_started.html'),
    'Deep Learning': (4, 'Understand neural networks and train your first deep models.', 'Kaggle: Intro to Deep Learning', 'https://www.kaggle.com/learn/intro-to-deep-learning'),
}

# career title: (description, skills in learning order; also the required skills)
CAREERS = {
    'Full Stack Developer': (
        'Build complete web applications, from the user interface to the server and database.',
        ['HTML', 'CSS', 'JavaScript', 'Git', 'React', 'Node.js', 'Express.js', 'MongoDB', 'REST API'],
    ),
    'Frontend Developer': (
        'Create fast, responsive and attractive user interfaces for websites and web apps.',
        ['HTML', 'CSS', 'JavaScript', 'Git', 'React', 'Tailwind CSS', 'Testing'],
    ),
    'Backend Developer': (
        'Design APIs, manage databases and keep the server side of applications secure and fast.',
        ['Git', 'Node.js', 'Express.js', 'REST API', 'MongoDB', 'SQL', 'JWT'],
    ),
    'Data Analyst': (
        'Clean data, find patterns and present insights through reports and dashboards.',
        ['Python', 'SQL', 'Excel', 'Pandas', 'Statistics', 'Data Visualization'],
    ),
    'AI/ML Engineer': (
        'Build, train and test machine learning models that solve real-world problems.',
        ['Python', 'NumPy', 'Pandas', 'Statistics', 'Machine Learning', 'Scikit-learn', 'Deep Learning'],
    ),
}


class Command(BaseCommand):
    help = 'Load careers, their skills and roadmap steps'

    def handle(self, *args, **options):
        for title, (description, skill_names) in CAREERS.items():
            career, _ = Career.objects.update_or_create(
                title=title, defaults={'description': description}
            )

            skills = [Skill.objects.get_or_create(name=n)[0] for n in skill_names]
            career.required_skills.set(skills)

            RoadmapStep.objects.filter(career=career).delete()
            for order, name in enumerate(skill_names, start=1):
                weeks, desc, res_title, res_url = LIBRARY[name]
                RoadmapStep.objects.create(
                    career=career,
                    order=order,
                    skill=name,
                    description=desc,
                    weeks=weeks,
                    resource_title=res_title,
                    resource_url=res_url,
                )

        self.stdout.write(self.style.SUCCESS(f'Loaded {len(CAREERS)} careers with roadmaps'))