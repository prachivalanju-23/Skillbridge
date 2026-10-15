from resume.models import SkillGap, StudentSkill


def save_gap(user, career):
    required = list(career.required_skills.values_list('name', flat=True))
    mine = {n.lower() for n in StudentSkill.objects.filter(user=user).values_list('skill__name', flat=True)}
    matched = [s for s in required if s.lower() in mine]
    missing = [s for s in required if s.lower() not in mine]
    percentage = round(len(matched) / len(required) * 100) if required else 0
    gap, _ = SkillGap.objects.update_or_create(
        user=user, career=career,
        defaults={'matched': matched, 'missing': missing, 'percentage': percentage},
    )
    return gap, required