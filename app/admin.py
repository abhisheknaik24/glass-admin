from django.contrib import admin

from app.models import Cart, Feature, Item, Notification, Production, WorkOrder

admin.site.register(Item)
admin.site.register(Feature)
admin.site.register(Cart)
admin.site.register(Notification)
admin.site.register(WorkOrder)
admin.site.register(Production)
