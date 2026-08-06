from celery import shared_task
from django.contrib.auth import get_user_model

from .llm import generate_welcome_email
from .services import send_and_log

User = get_user_model() #This method will return the currently active user model

@shared_task
def send_welcome_email_task(user_id, course_id):
    """
    Background task: build + send a personalized Day-1 welcome email.
    """

    from courses.models import Course, PersonalizedLearningPath, Module
    from assessments.models import Assessment,AssessmentSubmission

    # Imported inside the function to avoid circular imports at startup.
    user = User.objects.get(id=user_id)
    course = Course.objects.get(id=course_id)

    # 1) First module in their personalized path (fallback: first by order)
    path = PersonalizedLearningPath.objects.filter(user=user,course=course).first()

    #module
    if path and path.path_data:
        first_module_title = path.path_data[0].get('title', 'your first module')
    else:
        first_mod = Module.objects.filter(course=course).order_by('order').first()
        first_module_title = first_mod.title  

    #module
    # module = Module.objects.filter(course=course).first()

    #weak skills
    weak_skills = []

    #onboarding
    onboarding = Assessment.objects.filter(course=course,is_onboarding=True).first()
    
    if onboarding:
        sub = AssessmentSubmission.objects.filter(user=user,assessment=onboarding).first()
        if sub and sub.skill_scores:
            weak_skills = [skill for skill, pct in sub.skill_scores.items() if pct < 70]

    email = generate_welcome_email(user.username, course.title, first_module_title, weak_skills)
    recipient = user.email or f"{user.username}@example.com"
    log = send_and_log(user, recipient, "welcome", email["subject"], email["body"])

    return {"log_id" : log.id, "status": log.status}












# @shared_task
# def add(z, y):
#     print(f"Task Add({z} and {y}) is running")
#     return z + y
