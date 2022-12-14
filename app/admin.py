from django.contrib import admin

from app.models import (
    Cart,
    Feature,
    Inventory,
    Item,
    Notification,
    Production,
    Sidebar,
    WorkOrder,
)

admin.site.register(Sidebar)
admin.site.register(Item)
admin.site.register(Feature)
admin.site.register(Inventory)
admin.site.register(Cart)
admin.site.register(Notification)
admin.site.register(WorkOrder)
admin.site.register(Production)
