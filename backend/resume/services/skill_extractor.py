import re

SKILLS = [
    'HTML', 'CSS', 'JavaScript', 'TypeScript', 'React', 'Angular', 'Vue', 'Node.js', 'Express.js',
    'MongoDB', 'MySQL', 'SQL', 'PostgreSQL', 'Python', 'Java', 'C++', 'C#', 'PHP', 'Django', 'Flask',
    'FastAPI', 'Spring Boot', 'Hibernate', 'Maven', 'REST API', 'JWT', 'Git', 'GitHub', 'Docker', 'AWS',
    'Bootstrap', 'Tailwind', 'Redux', 'Pandas', 'NumPy', 'Scikit-learn', 'Machine Learning',
    'Deep Learning', 'NLP', 'TensorFlow', 'Excel', 'Power BI', 'Tableau', 'Statistics',
    'Data Visualization', 'Responsive Design', 'JSP', 'Servlets', 'Postman', 'Linux', 'Firebase',
]

ALIASES = {
    'nodejs': 'Node.js', 'node js': 'Node.js', 'expressjs': 'Express.js',
    'reactjs': 'React', 'react.js': 'React', 'mongo': 'MongoDB', 'html5': 'HTML', 'css3': 'CSS',
    'restful api': 'REST API', 'rest apis': 'REST API', 'sklearn': 'Scikit-learn',
    'natural language processing': 'NLP', 'ml': 'Machine Learning',
}

HEADINGS = {
    'education': ['education', 'academic details', 'academics', 'qualification', 'educational qualification'],
    'projects': ['projects', 'project', 'academic projects', 'personal projects'],
    'certifications': ['certifications', 'certification', 'certificates', 'courses', 'achievements'],
    'experience': ['experience', 'work experience', 'internship', 'internships', 'professional experience'],
    'skills': ['skills', 'technical skills', 'key skills'],
}


def _has(text, term):
    pattern = r'(?<![a-z0-9+#.])' + re.escape(term.lower()) + r'(?![a-z0-9+#])'
    return re.search(pattern, text) is not None


def extract_skills(text):
    t = text.lower()
    found = [s for s in SKILLS if _has(t, s)]
    for alias, skill in ALIASES.items():
        if skill not in found and _has(t, alias):
            found.append(skill)
    return found


def split_sections(text):
    sections = {'education': [], 'projects': [], 'certifications': [], 'experience': []}
    current = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        clean = re.sub(r'[^a-z ]', '', line.lower()).strip()
        key = next((k for k, words in HEADINGS.items() if clean in words), None)
        if key and len(line) < 35:
            current = key
            continue
        if current in sections:
            sections[current].append(line)
    return sections


def extract_basics(text):
    email = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    phone = re.search(r'(\+?\d[\d\s-]{8,13}\d)', text)
    lines = [l.strip() for l in text.splitlines() if l.strip()][:5]
    name = next((l for l in lines
                 if re.fullmatch(r'[A-Za-z. ]{3,40}', l) and len(l.split()) <= 4), '')
    return {
        'name': name.title() if name.isupper() else name,
        'email': email.group(0) if email else '',
        'phone': phone.group(0).strip() if phone else '',
    }


def parse_resume(text):
    data = extract_basics(text)
    data['skills'] = extract_skills(text)
    data.update(split_sections(text))
    return data