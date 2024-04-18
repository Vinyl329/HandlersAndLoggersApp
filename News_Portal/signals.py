from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
import datetime

from .models import PostCategory, Post, Category
from django.conf import settings


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {'text': preview,
         'link': f'{settings.SITE_URL}/news/{pk}',
         }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):  # check subscribers=None
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)

def weekly_mailing():  # вынести в utils
    #  Your job processing logic here...
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(pub_date__gte=last_week)  # lookup __gte
    categories = set(posts.values_list('category__name', flat=True))
    categories.remove(None)
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'mailing/weekly_news.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )

    # время отправки без микросекунд для заголовка
    sending_time = datetime.datetime.now().replace(microsecond=0)

    msg = EmailMultiAlternatives(
        subject=f'News from last week {sending_time}',  # тема письма
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    print(f'msg sent {sending_time}')