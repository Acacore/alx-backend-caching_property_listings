from celery import shared_task

@shared_task
def my_background_task(arg1, arg2):
    # Perform your long-running operation here
    return f"Task completed with {arg1} and {arg2}"