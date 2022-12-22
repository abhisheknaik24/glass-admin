from celery import shared_task

from app.models import Cart, Feature, Item, Notification, Production, Sidebar, WorkOrder


@shared_task
def work_order_to_production():
    work_orders = WorkOrder.objects.filter(is_active=True)

    if work_orders:
        for i in work_orders:
            if not Production.objects.filter(work_order__id=i.id).exists():
                productions = Production.objects.filter(work_order__id=i.id)
                if productions:
                    for j in productions:
                        if (
                            j.is_cutting == True
                            and j.is_polishing == False
                            and j.is_fabrication == False
                            and j.is_toughening == False
                            and j.is_dgu == False
                        ):
                            polishing_production = Production.objects.filter(
                                id=j.id
                            ).update(is_polishing=True)
                        elif (
                            j.is_cutting == True
                            and j.is_polishing == True
                            and j.is_fabrication == False
                            and j.is_toughening == False
                            and j.is_dgu == False
                        ):
                            fabrication_production = Production.objects.filter(
                                id=j.id
                            ).update(is_fabrication=True)
                        elif (
                            j.is_cutting == True
                            and j.is_polishing == True
                            and j.is_fabrication == True
                            and j.is_toughening == False
                            and j.is_dgu == False
                        ):
                            toughening_production = Production.objects.filter(
                                id=j.id
                            ).update(is_toughening=True)
                        elif (
                            j.is_cutting == True
                            and j.is_polishing == True
                            and j.is_fabrication == True
                            and j.is_toughening == True
                            and j.is_dgu == False
                        ):
                            dgu_production = Production.objects.filter(id=j.id).update(
                                is_dgu=True
                            )
                        else:
                            pass
                else:
                    cutting_production = Production(
                        work_order=i,
                        actual_qty=i.quantity,
                        balance_qty=i.quantity,
                        produce_qty=0,
                        status="cutting",
                    )
                    cutting_production.save()
    return True
