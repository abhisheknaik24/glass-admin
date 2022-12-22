from celery import shared_task

from app.models import Cart, Feature, Item, Notification, Production, Sidebar, WorkOrder


@shared_task
def work_order_to_production():
    work_orders = WorkOrder.objects.filter(is_active=True)
    print("work_orders", work_orders)
    # if work_orders:
    #     production = Production()
    return True
