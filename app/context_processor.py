from app.models import Cart, Notification, Sidebar


def index_processor(request):
    sidebar, carts, notifications = ([] for i in range(3))
    total_price, total_rate, total_discount = (0 for i in range(3))

    if request.user.is_authenticated:
        try:
            if request.user.groups.values_list() is not None:
                groups = list(request.user.groups.values_list())

                sidebar = list(Sidebar.objects.filter(group__in=groups))

            carts = Cart.objects.filter(user=request.user.id)

            for i in carts:
                total_price += i.total_price
                total_rate += i.total_rate
                total_discount += i.total_discount

            notifications = Notification.objects.all()[:5]

        except Exception as e:
            raise e

    context = {
        "sidebar": sidebar,
        "carts": carts,
        "total_price": total_price,
        "total_rate": total_rate,
        "total_discount": total_discount,
        "notifications": notifications,
    }

    return context
