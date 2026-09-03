from django.utils import timezone

def recency_score(last_active):
    """
    Turn a last_active timestamp into a Score (0-100)
    """

    if not last_active:
        return 0

    days = (timezone.now() - last_active).days

    if days <= 3:
        return 100
    if days <= 7:
        return 70
    if days <= 14:
        return 40
    if days <= 30:
        return 20
    return 5


def compute_health_score(completion_pct, last_active, module_score_pct):
    """
    Learner's health score
    """

    recency = recency_score(last_active)
    score = (completion_pct * 0.5) + (recency * 0.3) + (module_score_pct * 0.2)
    return round(score)


def health_status(score):
    return "healthy" if score >= 50 else "at_risk"