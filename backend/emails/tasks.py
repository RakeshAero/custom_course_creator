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


@shared_task
def send_weekly_summary_task(user_id, course_id):
    """
    Background task: build + send a personalized weekly progress email.
    """
    # Imported inside the function to avoid circular imports at startup.
    from courses.models import Course, Subtopic
    from progress.models import SubtopicProgress
    from .llm import generate_weekly_summary_email

    user = User.objects.get(id=user_id)
    course = Course.objects.get(id=course_id)

    subtopics = list(
        Subtopic.objects.filter(module__course=course).order_by('module__order','order')    
    )

    total = len(subtopics)
    if total == 0:
        return {"skipped": "course has no subtopics"}

    completed_ids = set(
        SubtopicProgress.objects
        .filter(user=user, subtopic__in=subtopics, completed=True)
        .values_list('subtopic_id', flat=True)
    )
    completed_count = len(completed_ids)

    # Next step = first subtopic they haven't completed yet
    next_title = "You've completed everything -- great job!"
    for s in subtopics:
        if s.id not in completed_ids:
            next_title = s.title
            break

    email = generate_weekly_summary_email(user.username, course.title, completed_count, total, next_title)
    recipient = user.email or f"{user.username}@example.com"
    log = send_and_log(user, recipient, "weekly", email["subject"], email["body"])

    return {"log_id":log.id, "status": log.status}

@shared_task
def send_all_weekly_summaries():
    """
    The Monday cron TARGET. Doesn't send emails itself - it fans out one send_weekly_summary_task
    per active enrollment, so each email is its own task and one failure never blocks the rest.
    """

    from courses.models import CourseEnrollment

    pairs = CourseEnrollment.objects.filter(is_active=True).values_list('user_id','course_id')
    count = 0
    for user_id, course_id in pairs:
        send_weekly_summary_task.delay(user_id, course_id)
        count += 1
    return {"dispatched": count}
    









# @shared_task
# def add(z, y):
#     print(f"Task Add({z} and {y}) is running")
#     return z + y
