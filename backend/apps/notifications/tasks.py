from celery import shared_task
@shared_task
def send_push_notification(user_id, title, body): pass
