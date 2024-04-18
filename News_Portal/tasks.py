from celery import shared_task
from .models import Post
from .signals import send_notifications, weekly_mailing

@shared_task
def celery_new_posts_notification(pk):
    instance = Post.objects.get(pk=pk)
    categories = instance.category.all()
    subscribers = set()

    for cat in categories:
        subscribers = subscribers.union(cat.subscribers.all())

    send_notifications(instance.preview, instance.pk, instance.category, instance.title, subscribers)

@shared_task
def celery_weekly_mailing():
    weekly_mailing()