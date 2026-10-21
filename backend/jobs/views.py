from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Job
from .utils import job_to_dict


def parse_skills(value):
    return [s.strip() for s in (value or '').split(',') if s.strip()]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_list(request):
    jobs = Job.objects.prefetch_related('job_skills__skill').order_by('-id')

    category = request.query_params.get('category')
    level = request.query_params.get('level')
    if category:
        jobs = jobs.filter(category=category)
    if level:
        jobs = jobs.filter(level=level)

    user_skills = parse_skills(request.query_params.get('skills'))
    results = [job_to_dict(job, user_skills) for job in jobs]

    if user_skills:
        results.sort(key=lambda j: j['matchPercent'], reverse=True)

    return Response(results)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_detail(request, pk):
    job = get_object_or_404(Job.objects.prefetch_related('job_skills__skill'), pk=pk)
    user_skills = parse_skills(request.query_params.get('skills'))
    return Response(job_to_dict(job, user_skills))