from django.db import transaction
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import InterviewAnswer, InterviewQuestion, InterviewResult, InterviewSession
from .serializers import InterviewResultSerializer
from .services.answer_evaluator import evaluate_answer
from .services.question_generator import LEVELS, ROLES, generate_question

TOTAL = 5


def _avg(session, field):
    value = InterviewAnswer.objects.filter(question__session=session).aggregate(a=Avg(field))['a']
    return round(value or 0, 1)


# POST /api/interview/start/   body: {"role": "...", "level": "Beginner"}
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start(request):
    role = request.data.get('role')
    level = request.data.get('level')
    if role not in ROLES or level not in LEVELS:
        return Response({'detail': 'Valid role and level are required'}, status=400)

    difficulty = LEVELS.index(level) + 1
    q = generate_question(role, difficulty, [])
    with transaction.atomic():
        session = InterviewSession.objects.create(
            user=request.user, role=role, level=level,
            total_questions=TOTAL, current_difficulty=difficulty,
        )
        InterviewQuestion.objects.create(
            session=session, order=1, text=q['text'],
            difficulty=q['difficulty'], keywords=q['keywords'],
        )
    return Response(
        {'interview_id': session.id, 'number': 1, 'total': TOTAL, 'question': q['text']},
        status=201,
    )


# POST /api/interview/answer/   body: {"interview_id": 1, "answer": "..."}
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def answer(request):
    text = (request.data.get('answer') or '').strip()
    if not text:
        return Response({'detail': 'Answer is required'}, status=400)

    session = get_object_or_404(InterviewSession, pk=request.data.get('interview_id'), user=request.user)
    if session.status == 'completed':
        return Response({'detail': 'Interview already finished'}, status=400)

    current = session.questions.order_by('-order').first()
    if InterviewAnswer.objects.filter(question=current).exists():
        return Response({'detail': 'Question already answered'}, status=400)

    ev = evaluate_answer(current.keywords, text)

    with transaction.atomic():
        InterviewAnswer.objects.create(question=current, answer_text=text, **ev)

        # Last question: finish and save the result
        if current.order >= session.total_questions:
            overall = _avg(session, 'score')
            result = InterviewResult.objects.create(
                session=session, user=request.user,
                role=session.role, level=session.level,
                overall_score=overall,
                technical=_avg(session, 'technical'),
                communication=_avg(session, 'communication'),
                accuracy=_avg(session, 'accuracy'),
                summary=(
                    'Excellent performance. You are interview ready for this role.' if overall >= 8
                    else 'Good performance. Revise the missed points and practise longer answers.' if overall >= 5
                    else 'Needs improvement. Revise the core concepts and try again.'
                ),
            )
            session.status = 'completed'
            session.save()
            return Response({'evaluation': ev, 'finished': True, 'result_id': result.id})

        # Difficulty adjustment based on this score
        difficulty = session.current_difficulty
        if ev['score'] >= 7:
            difficulty = min(3, difficulty + 1)
        elif ev['score'] <= 4:
            difficulty = max(1, difficulty - 1)
        session.current_difficulty = difficulty
        session.save()

        asked = list(session.questions.values_list('text', flat=True))
        nxt = generate_question(session.role, difficulty, asked)
        InterviewQuestion.objects.create(
            session=session, order=current.order + 1, text=nxt['text'],
            difficulty=nxt['difficulty'], keywords=nxt['keywords'],
        )

    return Response({
        'evaluation': ev, 'finished': False,
        'number': current.order + 1, 'total': session.total_questions,
        'question': nxt['text'],
    })


# GET /api/interview/result/<id>/
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def result(request, pk):
    res = get_object_or_404(InterviewResult, pk=pk, user=request.user)
    questions = [
        {
            'text': q.text,
            'answer_text': q.answer.answer_text,
            'score': q.answer.score,
            'feedback': q.answer.feedback,
        }
        for q in res.session.questions.select_related('answer')
        if hasattr(q, 'answer')
    ]
    return Response({'result': InterviewResultSerializer(res).data, 'questions': questions})


# GET /api/interview/history/
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history(request):
    qs = InterviewResult.objects.filter(user=request.user).order_by('-created_at')
    return Response(InterviewResultSerializer(qs, many=True).data)