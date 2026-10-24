from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CATEGORIES, Answer, AptitudeTest, Question, TestResult
from .serializers import QuestionPublicSerializer, TestResultSerializer


# GET /api/aptitude/questions/?category=Logical
# No category = 5 random questions from each category (20 total)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def questions(request):
    category = request.query_params.get('category')
    if category:
        if category not in CATEGORIES:
            return Response({'detail': 'Invalid category'}, status=400)
        picked = list(Question.objects.filter(category=category).order_by('?')[:20])
    else:
        picked = []
        for cat in CATEGORIES:
            picked += list(Question.objects.filter(category=cat).order_by('?')[:5])
    return Response(QuestionPublicSerializer(picked, many=True).data)


# POST /api/aptitude/submit/   body: {"answers": [{"question_id": 1, "selected_index": 2}]}
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit(request):
    answers = request.data.get('answers')
    if not isinstance(answers, list) or not answers:
        return Response({'detail': 'answers list is required'}, status=400)

    ids = [a.get('question_id') for a in answers if isinstance(a, dict)]
    by_id = {q.id: q for q in Question.objects.filter(id__in=ids)}

    stats, checked, score = {}, [], 0
    for a in answers:
        if not isinstance(a, dict):
            continue
        q = by_id.pop(a.get('question_id'), None)  # pop: each question counts once
        if q is None:
            continue
        selected = a.get('selected_index')
        is_correct = selected == q.correct_index
        score += is_correct
        s = stats.setdefault(q.category, {'correct': 0, 'total': 0})
        s['total'] += 1
        s['correct'] += is_correct
        checked.append((q, selected, is_correct))

    if not checked:
        return Response({'detail': 'No valid answers found'}, status=400)

    category_scores = [
        {
            'category': cat,
            'correct': s['correct'],
            'total': s['total'],
            'percentage': round(s['correct'] / s['total'] * 100),
        }
        for cat, s in stats.items()
    ]

    with transaction.atomic():
        test = AptitudeTest.objects.create(user=request.user)
        Answer.objects.bulk_create(
            [Answer(test=test, question=q, selected_index=sel, is_correct=ok) for q, sel, ok in checked]
        )
        result = TestResult.objects.create(
            test=test,
            user=request.user,
            score=score,
            total=len(checked),
            category_scores=category_scores,
        )
    return Response(TestResultSerializer(result).data, status=201)


# GET /api/aptitude/results/  (newest first, only the logged-in student's)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def results(request):
    qs = TestResult.objects.filter(user=request.user).order_by('-created_at')
    return Response(TestResultSerializer(qs, many=True).data)