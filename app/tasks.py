from celery import shared_task

from app.models import Cart, Feature, Item, Notification, Production, WorkOrder


@shared_task
def work_order_to_production():
    work_orders = WorkOrder.objects.filter(is_active=True)

    if work_orders:
        for i in work_orders:
            if not Production.objects.filter(work_order__id=i.id).exists():
                cutting_production = Production(
                    work_order=i,
                    status="cutting",
                )
                cutting_production.save()
    return True


@shared_task
def production_to_inventory():
    return True
