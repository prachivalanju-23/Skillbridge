def score_resume(p):
    breakdown = {
        'skills': min(len(p['skills']) * 4, 40),
        'education': 15 if p['education'] else 0,
        'projects': 15 if p['projects'] else 0,
        'certifications': 10 if p['certifications'] else 0,
        'experience': 10 if p['experience'] else 0,
        'contact': (5 if p['email'] else 0) + (5 if p['phone'] else 0),
    }
    return sum(breakdown.values()), breakdown