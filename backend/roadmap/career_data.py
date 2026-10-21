# Icon names and colours are used by the React Career Goal page
CAREER_STYLE = {
    'Full Stack Developer': {'icon': 'Layers', 'color': '#fde7d6'},
    'Frontend Developer': {'icon': 'Monitor', 'color': '#d9f5e8'},
    'Backend Developer': {'icon': 'Server', 'color': '#e6e0fb'},
    'Data Analyst': {'icon': 'BarChart3', 'color': '#dbeefc'},
    'AI/ML Engineer': {'icon': 'Brain', 'color': '#fbe0ec'},
}
DEFAULT_STYLE = {'icon': 'Briefcase', 'color': '#e6e0fb'}


def career_to_dict(career):
    style = CAREER_STYLE.get(career.title, DEFAULT_STYLE)
    return {
        'id': career.id,
        '_id': str(career.id),
        'name': career.title,
        'description': career.description,
        'requiredSkills': [s.name for s in career.required_skills.all()],
        'icon': style['icon'],
        'color': style['color'],
    }