from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

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
    productions = Production.objects.filter(status="dispatch", is_active=True)

    if productions:
        for i in productions:
            try:
                item = Item.objects.get(id=i.work_order.item.id, is_active=True)
                if item:
                    item.in_stock += i.work_order.quantity
                    item.save()

                    try:
                        production = Production.objects.get(id=i.id)
                        if production:
                            production.is_active = False
                            production.save()
                    except ObjectDoesNotExist:
                        production = None
            except ObjectDoesNotExist:
                item = None
    return True
