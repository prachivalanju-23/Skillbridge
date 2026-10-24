import re


def _clamp(n):
    return max(0, min(10, n))


def _round(x):
    return int(x + 0.5)


def evaluate_answer(keywords, answer):
    """Score an answer by keyword matching.
    MOCK: to use a real AI later, keep this signature and change the inside."""
    text = answer.lower()
    words = len(answer.split())
    matched = [k for k in keywords if k in text]
    missing = [k for k in keywords if k not in text]
    ratio = len(matched) / len(keywords) if keywords else 0

    accuracy = _clamp(_round(ratio * 12))
    technical = _clamp(_round(ratio * 10) + (1 if words >= 40 else 0))
    if words < 5:
        communication = 2
    elif words < 15:
        communication = 4
    elif words < 30:
        communication = 6
    elif words <= 120:
        communication = 8
    else:
        communication = 7
    if re.search(r'[.!?]', answer):
        communication = _clamp(communication + 1)

    score = _clamp(_round(technical * 0.4 + accuracy * 0.3 + communication * 0.3))

    if score >= 8:
        feedback = 'Excellent answer. You covered the key points clearly.'
    elif score >= 5:
        feedback = 'Good explanation, but it can be more complete.'
    else:
        feedback = 'This answer needs more depth.'
    if missing:
        feedback += ' Try to also mention: ' + ', '.join(missing[:3]) + '.'
    if words < 15:
        feedback += ' Give a longer answer with an example.'

    return {
        'score': score,
        'technical': technical,
        'communication': communication,
        'accuracy': accuracy,
        'feedback': feedback,
    }