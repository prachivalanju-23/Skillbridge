from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Skill, Career
from .models import Resume, StudentProfile, StudentSkill, SkillGap
from .services.text_extractor import extract_text
from .services.skill_extractor import parse_resume
from .services.resume_scorer import score_resume
from .services.skill_gap import save_gap

MAX_SIZE = 5 * 1024 * 1024


def build_profile(user):
    profile = StudentProfile.objects.filter(user=user).first()
    if not profile:
        return None
    resume = Resume.objects.filter(user=user).order_by('-uploaded_at').first()
    gap = SkillGap.objects.filter(user=user).select_related('career').order_by('-updated_at').first()
    return {
        'name': profile.name, 'email': profile.email, 'phone': profile.phone,
        'education': profile.education, 'projects': profile.projects,
        'certifications': profile.certifications, 'experience': profile.experience,
        'resume_score': profile.resume_score,
        'score_breakdown': resume.score_breakdown if resume else {},
        'skills': sorted(StudentSkill.objects.filter(user=user).values_list('skill__name', flat=True)),
        'target_role': gap.career.title if gap else None,
        'skill_gap': {'matched': gap.matched, 'missing': gap.missing,
                      'percentage': gap.percentage} if gap else None,
    }


class ResumeUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get('resume')
        if not file:
            return Response({'message': 'No file uploaded'}, status=400)
        if not file.name.lower().endswith(('.pdf', '.docx')):
            return Response({'message': 'Only PDF and DOCX files are allowed'}, status=400)
        if file.size > MAX_SIZE:
            return Response({'message': 'File too large (max 5 MB)'}, status=400)

        try:
            text = extract_text(file)
        except Exception:
            return Response({'message': 'Could not read this file'}, status=400)
        if len(text.strip()) < 30:
            return Response({'message': 'No readable text found (scanned PDF?)'}, status=400)

        parsed = parse_resume(text)
        total, breakdown = score_resume(parsed)
        user = request.user

        with transaction.atomic():
            Resume.objects.create(user=user, file_name=file.name, raw_text=text,
                                  score=total, score_breakdown=breakdown)
            StudentProfile.objects.update_or_create(user=user, defaults={
                'name': parsed['name'] or user.first_name, 'email': parsed['email'],
                'phone': parsed['phone'], 'education': parsed['education'],
                'projects': parsed['projects'], 'certifications': parsed['certifications'],
                'experience': parsed['experience'], 'resume_score': total,
            })
            StudentSkill.objects.filter(user=user).delete()
            for skill_name in parsed['skills']:
                skill, _ = Skill.objects.get_or_create(name=skill_name)
                StudentSkill.objects.create(user=user, skill=skill)

            old_gap = SkillGap.objects.filter(user=user).order_by('-updated_at').first()
            if old_gap:
                save_gap(user, old_gap.career)

        return Response(build_profile(user), status=201)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = build_profile(request.user)
        if data is None:
            return Response({'message': 'No resume uploaded yet'}, status=404)
        return Response(data)


class RolesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response([{'id': c.id, 'title': c.title} for c in Career.objects.order_by('title')])


class SkillGapView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        career = get_object_or_404(Career, pk=request.data.get('career_id'))
        if not StudentSkill.objects.filter(user=request.user).exists():
            return Response({'message': 'Upload your resume first'}, status=400)
        gap, required = save_gap(request.user, career)
        return Response({'target_role': career.title, 'required': required,
                         'matched': gap.matched, 'missing': gap.missing,
                         'percentage': gap.percentage})