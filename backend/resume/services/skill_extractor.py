import re

SKILLS = [
    'HTML', 'CSS', 'JavaScript', 'TypeScript', 'React', 'Angular', 'Vue', 'Node.js', 'Express.js',
    'MongoDB', 'MySQL', 'SQL', 'PostgreSQL', 'Python', 'Java', 'C++', 'C#', 'PHP', 'Django', 'Flask',
    'FastAPI', 'Spring Boot', 'Hibernate', 'Maven', 'REST API', 'JWT', 'Git', 'GitHub', 'Docker', 'AWS',
    'Bootstrap', 'Tailwind', 'Redux', 'Pandas', 'NumPy', 'Scikit-learn', 'Machine Learning',
    'Deep Learning', 'NLP', 'TensorFlow', 'Excel', 'Power BI', 'Tableau', 'Statistics',
    'Data Visualization', 'Responsive Design', 'JSP', 'Servlets', 'Postman', 'Linux', 'Firebase',
    'Android Studio', 'Android', 'Kotlin', 'XML', 'Eclipse', 'Tomcat', 'JDBC', 'VS Code',
    'Software Testing', 'Figma', 'Canva', 'Jira', 'Selenium', 'OOP', 'Data Structures',
]

ALIASES = {
    'nodejs': 'Node.js', 'node js': 'Node.js', 'expressjs': 'Express.js',
    'reactjs': 'React', 'react.js': 'React', 'mongo': 'MongoDB', 'html5': 'HTML', 'css3': 'CSS',
    'restful api': 'REST API', 'rest apis': 'REST API', 'sklearn': 'Scikit-learn',
    'natural language processing': 'NLP', 'ml': 'Machine Learning',
    'servlet': 'Servlets', 'apache tomcat': 'Tomcat', 'visual studio code': 'VS Code',
    'bug finding': 'Software Testing', 'bug-finding': 'Software Testing',
    'object oriented programming': 'OOP', 'dsa': 'Data Structures',
}

# Headings whose content we store
HEADINGS = {
    'education': ['education', 'academic details', 'academics', 'qualification',
                  'educational qualification', 'academic qualification'],
    'projects': ['projects', 'project', 'academic projects', 'personal projects'],
    'certifications': ['certifications', 'certification', 'certificates', 'courses'],
    'experience': ['experience', 'work experience', 'internship', 'internships',
                   'professional experience'],
    'skills': ['skills', 'technical skills', 'key skills'],
}

# Headings we recognise but do not store. They only END the previous section.
OTHER_HEADINGS = [
    'career objective', 'objective', 'summary', 'professional summary', 'profile',
    'soft skills', 'languages', 'language', 'hobbies', 'interests', 'declaration',
    'personal details', 'references', 'contact', 'links',
    'achievements', 'achievements activities', 'achievements and activities',
]

ALL_HEADINGS = (
    {w for words in HEADINGS.values() for w in words}
    | set(OTHER_HEADINGS)
    | {'resume', 'curriculum vitae', 'cv'}
)

# Short phrases that look like a name but are not
NOT_NAMES = {
    'communication', 'teamwork', 'leadership management', 'leadership', 'adaptability',
    'time management', 'problem solving', 'critical thinking', 'web technologies',
    'software tools', 'programming languages',
}

# Words that mean a line is not a person's name
NOT_NAME_WORDS = {
    'app', 'project', 'system', 'website', 'portal', 'application', 'developer',
    'engineer', 'student', 'resume', 'technologies', 'management', 'college',
    'university', 'bachelor', 'master',
}

BULLET_CHARS = '•●▪■◦○-–—*·➢➤✓'


def _norm(line):
    return re.sub(r'\s+', ' ', re.sub(r'[^a-z ]', ' ', line.lower())).strip()


def _clean_line(line):
    return line.strip().lstrip(BULLET_CHARS).strip()


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
        line = _clean_line(raw)
        if not line:
            continue
        clean = _norm(line)
        if len(line) < 40:
            key = next((k for k, words in HEADINGS.items() if clean in words), None)
            if key:
                current = key
                continue
            if clean in OTHER_HEADINGS:
                current = None
                continue
        if current in sections:
            sections[current].append(line)
    return sections


def extract_basics(text, file_name=''):
    email = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text)
    phone = re.search(r'(\+?\d[\d\s-]{8,13}\d)', text)

    # candidate name lines from the top of the resume
    lines = [_clean_line(l) for l in text.splitlines() if l.strip()][:15]
    candidates = [
        l for l in lines
        if re.fullmatch(r'[A-Za-z. ]{3,40}', l)
        and 2 <= len(l.split()) <= 4
        and _norm(l) not in ALL_HEADINGS
        and _norm(l) not in NOT_NAMES
    ]

    # best hint: the name also appears in the file name or the email address
    hint = (file_name.rsplit('.', 1)[0] + ' ' + (email.group(0).split('@')[0] if email else '')).lower()
    name = ''
    for c in candidates:
        tokens = [t for t in re.split(r'[^a-z]+', c.lower()) if len(t) >= 3]
        if tokens and sum(t in hint for t in tokens) >= min(2, len(tokens)):
            name = c
            break

    # fallback: first candidate that does not look like a project or a title
    if not name:
        for c in candidates:
            if not (set(_norm(c).split()) & NOT_NAME_WORDS):
                name = c
                break

    return {
        'name': name.title() if name.isupper() else name,
        'email': email.group(0) if email else '',
        'phone': phone.group(0).strip() if phone else '',
    }


def parse_resume(text, file_name=''):
    data = extract_basics(text, file_name)
    data['skills'] = extract_skills(text)
    data.update(split_sections(text))
    return data