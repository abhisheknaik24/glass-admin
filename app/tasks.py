import pandas
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

                try:
                    work_order = WorkOrder.objects.get(id=i.id, is_active=True)
                    if work_order:
                        work_order.is_active = False
                        work_order.save()
                except ObjectDoesNotExist:
                    work_order = None
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
                        production = Production.objects.get(id=i.id, is_active=True)
                        if production:
                            production.is_active = False
                            production.save()
                    except ObjectDoesNotExist:
                        production = None
            except ObjectDoesNotExist:
                item = None
    return True


@shared_task
def excel_to_item():
    excel_data_df = pandas.read_excel("resources/Item.xlsx")

    if excel_data_df:
        for index, row in excel_data_df.iterrows():
            item = Item(
                name=row["Item Name"],
                rate=row["Rate"],
                discount_percentage=10,
                unit=row["Unit"],
                height=row["Height"],
                width=row["Width"],
            )
            item.save()
    return True
