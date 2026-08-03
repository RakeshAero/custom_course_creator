from celery import shared_task

@shared_task
def add(z, y):
    print(f"Task Add({z} and {y}) is running")
    return z + y
