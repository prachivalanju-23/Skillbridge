import math

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Career
from .career_data import career_to_dict
from .models import CareerGoal, RoadmapStep


def parse_skills(value):
    return [s.strip().lower() for s in (value or '').split(',') if s.strip()]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def career_list(request):
    careers = Career.objects.prefetch_related('required_skills').order_by('title')
    return Response([career_to_dict(c) for c in careers])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def career_detail(request, pk):
    career = get_object_or_404(Career.objects.prefetch_related('required_skills'), pk=pk)
    return Response(career_to_dict(career))


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def career_goal(request):
    if request.method == 'POST':
        try:
            career_id = int(request.data.get('career_id'))
        except (TypeError, ValueError):
            return Response({'message': 'career_id is required'}, status=400)

        career = get_object_or_404(Career, pk=career_id)
        goal, _ = CareerGoal.objects.update_or_create(
            user=request.user, defaults={'career': career}
        )
    else:
        goal = CareerGoal.objects.filter(user=request.user).first()
        if goal is None:
            return Response({'career_id': None, 'career': None})

    career = Career.objects.prefetch_related('required_skills').get(pk=goal.career_id)
    return Response({'career_id': goal.career_id, 'career': career_to_dict(career)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def roadmap_for_career(request, career_id):
    career = get_object_or_404(Career, pk=career_id)
    db_steps = list(RoadmapStep.objects.filter(career=career).order_by('order'))
    if not db_steps:
        return Response({'message': 'Roadmap not found for this career'}, status=404)

    user_skills = parse_skills(request.query_params.get('skills'))

    week = 1
    steps = []
    for step in db_steps:
        done = step.skill.lower() in user_skills
        if done:
            start_week = None
            end_week = None
        else:
            start_week = week
            week += step.weeks
            end_week = week - 1

        steps.append(
            {
                'order': step.order,
                'skill': step.skill,
                'description': step.description,
                'weeks': step.weeks,
                'resourceTitle': step.resource_title,
                'resourceUrl': step.resource_url,
                'done': done,
                'startWeek': start_week,
                'endWeek': end_week,
            }
        )

    total_steps = len(steps)
    completed = sum(1 for s in steps if s['done'])
    total_weeks = week - 1

    return Response(
        {
            'careerId': career.id,
            'careerName': career.title,
            'steps': steps,
            'totalSteps': total_steps,
            'completedSteps': completed,
            'progressPercent': int(completed / total_steps * 100 + 0.5),
            'totalWeeks': total_weeks,
            'totalMonths': math.ceil(total_weeks / 4),
        }
    )