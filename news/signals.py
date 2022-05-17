from datetime import datetime

from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.core.mail import mail_admins, EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPaper import settings
from .models import Post


@receiver(m2m_changed, sender=Post.cats.through)
def notify_sub(sender, instance, **kwargs):
    html_content = render_to_string('created_msg.html', {'post': instance, })
    category = instance.cats.all()
    emails = set()
    for cat in category:
        emails |= cat.get_emails()
    msg = EmailMultiAlternatives(
        subject=f'Здравствуй. Новая статья в твоём любимом разделе!',
        body=instance.text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=emails,
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()


@receiver(pre_save, sender=Post)
def check_post_today(sender, instance, **kwargs):
    today_posts = Post.objects.filter(created__date=datetime.now().date())
    return len(today_posts)
