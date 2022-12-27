import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from app.tasks import production_to_inventory, work_order_to_production

logger = logging.getLogger(__name__)


def work_order_to_production_task():
    work_order_to_production.delay()
    logger.info("Work order to production process trigger successfully.")


def production_to_inventory_task():
    production_to_inventory.delay()
    logger.info("Production to inventory process trigger successfully.")


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            work_order_to_production_task,
            trigger=CronTrigger(minute="*"),
            id="work_order_to_production",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            production_to_inventory_task,
            trigger=CronTrigger(minute="*"),
            id="production_to_inventory",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
