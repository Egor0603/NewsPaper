import datetime

from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPaper import settings
from news.models import Post, Category


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def notif_users():
    from_time = datetime.datetime.now() - datetime.timedelta(7)
    posts = Post.objects.filter(created__gte=from_time)

    for category in Category.objects.all():
        html_content = render_to_string('created_msg.html', {'post': posts, 'cats': category})
        msg = EmailMultiAlternatives(
        subject=f'Weekly articles!',
        body=Post.text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=category.get_emails()
        )
        print('YES!')

        msg.attach_alternative(html_content, "text/html")
        msg.send()
