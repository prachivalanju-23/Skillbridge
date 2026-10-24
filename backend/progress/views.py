from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from aptitude.models import TestResult
from interview.models import InterviewResult


# GET /api/progress/
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def progress(request):
    tests = list(TestResult.objects.filter(user=request.user).order_by('-created_at'))
    interviews = list(InterviewResult.objects.filter(user=request.user).order_by('-created_at'))

    aptitude = {'attempts': 0, 'latest_percent': None, 'best_percent': None, 'categories': []}
    if tests:
        percents = [round(t.score / t.total * 100) for t in tests]
        aptitude = {
            'attempts': len(tests),
            'latest_percent': percents[0],
            'best_percent': max(percents),
            'categories': [
                {'category': c['category'], 'percentage': c['percentage']}
                for c in tests[0].category_scores
            ],
        }

    interview = {'attempts': 0, 'latest_score': None, 'average_score': None}
    if interviews:
        interview = {
            'attempts': len(interviews),
            'latest_score': interviews[0].overall_score,
            'average_score': round(sum(i.overall_score for i in interviews) / len(interviews), 1),
        }

    roadmap = {'percent': None}  # placeholder until the roadmap module is connected
    skills = [
        {'name': 'React', 'percent': 90},
        {'name': 'JavaScript', 'percent': 80},
        {'name': 'Python', 'percent': 60},
        {'name': 'MySQL', 'percent': 50},
    ]

    parts = []
    if aptitude['latest_percent'] is not None:
        parts.append(aptitude['latest_percent'])
    if interview['average_score'] is not None:
        parts.append(interview['average_score'] * 10)
    overall = round(sum(parts) / len(parts)) if parts else 0

    achievements = [
        {'title': 'First Aptitude Test', 'earned': aptitude['attempts'] >= 1},
        {'title': 'Aptitude Pro (80%+)', 'earned': (aptitude['best_percent'] or 0) >= 80},
        {'title': 'First Mock Interview', 'earned': interview['attempts'] >= 1},
        {'title': 'Interview Star (8+/10)', 'earned': (interview['latest_score'] or 0) >= 8},
    ]

    return Response({
        'overall': overall, 'aptitude': aptitude, 'interview': interview,
        'roadmap': roadmap, 'skills': skills, 'achievements': achievements,
    })