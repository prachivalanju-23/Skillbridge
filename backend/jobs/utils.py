def job_to_dict(job, user_skills=None):
    required = [js.skill.name for js in job.job_skills.all()]

    data = {
        'id': job.id,
        '_id': str(job.id),
        'title': job.title,
        'company': job.company,
        'location': job.location,
        'jobType': job.job_type,
        'experienceLevel': job.level,
        'careerCategory': job.category,
        'description': job.description,
        'requiredSkills': required,
        'applyLink': job.apply_link,
    }

    if user_skills:
        lower = [s.lower() for s in user_skills]
        matched = [s for s in required if s.lower() in lower]
        missing = [s for s in required if s.lower() not in lower]
        data['matchPercent'] = (
            int(len(matched) / len(required) * 100 + 0.5) if required else 0
        )
        data['matchedSkills'] = matched
        data['missingSkills'] = missing

    return data