import datetime
import logging
import warnings
from django.utils import timezone

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Category, Post

# Ignore dateparser warnings regarding pytz
warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)
logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    time_delta = datetime.timedelta(7)
    start_date = datetime.datetime.now(tz=timezone.utc) - time_delta
    end_date = datetime.datetime.now(tz=timezone.utc)
    recent_posts = Post.objects.filter(created__range=(start_date, end_date))

    for category in Category.objects.all():
        html_content = render_to_string('created_msg.html',
                                        {'posts': recent_posts, 'categories': category}, )
        msg = EmailMultiAlternatives(
            subject=f'"You may be interested in this news"',
            body="News",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=category.get_emails())
        msg.attach_alternative(html_content, "text/html")
        msg.send()



# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"), #CronTrigger(second="*/5")
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")