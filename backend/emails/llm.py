import json
from google import genai
from google.genai import types
from django.conf import settings

def _client():
    return genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_welcome_email(learner_name, course_title, first_module_title, weak_skills):

    """
    Generates a personalized Day-1 welcome email.
    Returns {"subject" : str, "body": str}. Falls back to a template if the LLM fails.
    """
    prompt = f"""Write a short, warm Day-1 welcome email for an online learner.
                Learner's name: {learner_name}
                Course title: {course_title}
                Their personalized path starts with the module: {first_module_title}
                Skills area to focus on (their weak spots): {weak_skills}

                Requirements:
                - Friendly and encouraging, at most 3 short paragraphs.
                - Mention their name, the course, and that their path starts with "{first_module_title}".
                - Gently reference the focus areas.
                - Return a JSON object with exactly two keys: "subject" (string) and "body" (sting, plain text using \\n for line breaks).
             """

    try:
        client = _client()
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            content=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=800,
                response_mime_type="application/json",
            ),
        )
        data = json.loads(response.text)
        return {"subject": data["subject"],
                "body": data["body"],}
    except Exception as e:
        print(f"Error generating welcome email using LLM: {e}")

        return {
            "subject": f"Welcome to {course_title}, {learner_name}!",
            "body": (
                f"Hi {learner_name},\n\n"
                f"Welcome to {course_title}! We've built a personalized path just for you, "
                f"starting with \"{first_module_title}\".\n\n"
                f"A good area to focus on early: {weak_skills}. Your path is arranged to build "
                f"those up step by step.\n\nHappy learning!\nThe Learnify Team"
            ),
        }