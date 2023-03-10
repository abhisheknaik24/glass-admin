from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from app.models import Cart, Feature, Item, Notification, Production, WorkOrder


def login_view(request):
    return render(request, "login.html")


@login_required(login_url="/")
def products_view(request):
    if request.user.groups.filter(name__in=["Customer", "Admin"]).exists():
        items = Item.objects.filter(in_stock__gt=0, is_active=True)
        context = {"items": items}
        return render(request, "products.html", context)
    else:
        return redirect(login_view)


@login_required(login_url="/")
def product_details_view(request, id):
    if request.user.groups.filter(name__in=["Customer", "Admin"]).exists():
        try:
            item = Item.objects.get(id=id, is_active=True)
        except ObjectDoesNotExist:
            item = None
        features = Feature.objects.filter(item__id=id, is_active=True)
        context = {"item": item, "features": features}
        return render(request, "details.html", context)
    else:
        return redirect(login_view)


@login_required(login_url="/")
def products_cart_view(request):
    if request.user.groups.filter(name__in=["Customer"]).exists():
        return render(request, "cart.html")
    else:
        return redirect(login_view)


def add_to_cart(request, id):
    try:
        item = Item.objects.get(id=id, is_active=True)
        if item:
            cart_check = Cart.objects.filter(user=request.user, item=item).exists()
            if cart_check:
                cart = Cart.objects.get(user=request.user, item=item)
                cart.quantity += 1
                cart.save()
            else:
                cart = Cart(user=request.user, item=item, quantity=1)
                cart.save()
    except ObjectDoesNotExist:
        item = None
    return redirect(products_cart_view)


def increase_quantity(request, id):
    try:
        cart = Cart.objects.get(id=id, user=request.user)
        cart.quantity += 1
        cart.save()
    except ObjectDoesNotExist:
        cart = None
    return redirect(products_cart_view)


def decrease_quantity(request, id):
    try:
        cart = Cart.objects.get(id=id, user=request.user)
        cart.quantity -= 1
        if cart.quantity == 0:
            cart.delete()
        else:
            cart.save()
    except ObjectDoesNotExist:
        cart = None
    return redirect(products_cart_view)


def delete_cart(request, id):
    try:
        cart = Cart.objects.get(id=id, user=request.user)
        cart.delete()
    except ObjectDoesNotExist:
        cart = None
    return redirect(products_cart_view)


def clear_cart(request):
    cart = Cart.objects.filter(user=request.user)
    cart.delete()
    return redirect(products_cart_view)


def buy_now(request, id):
    try:
        cart = Cart.objects.get(id=id, user=request.user)
        cart.quantity += 1
        cart.save()
    except ObjectDoesNotExist:
        cart = None
    return redirect(products_checkout_view)


@login_required(login_url="/")
def products_checkout_view(request):
    if request.user.groups.filter(name__in=["Customer"]).exists():
        return render(request, "checkout.html")
    else:
        return redirect(login_view)


@login_required(login_url="/")
def work_order_view(request):
    if request.user.groups.filter(name__in=["Admin"]).exists():
        items = Item.objects.filter(is_active=True)
        work_orders = WorkOrder.objects.filter(is_active=True)
        context = {"items": items, "work_orders": work_orders}
        return render(request, "work_order.html", context)
    else:
        return redirect(login_view)


def add_work_order(request):
    if request.method == "POST":
        item_id = request.POST.get("item", None)
        quantity = request.POST.get("quantity", None)
        if item_id and quantity:
            try:
                item = Item.objects.get(id=item_id, is_active=True)
            except ObjectDoesNotExist:
                item = None
            if item:
                work_order = WorkOrder(item=item, quantity=quantity)
                work_order.save()
    return redirect(work_order_view)


@login_required(login_url="/")
def production_view(request):
    if request.user.groups.filter(name__in=["Admin"]).exists():
        productions = Production.objects.filter(is_active=True)
        context = {"productions": productions}
        return render(request, "production.html", context)
    else:
        return redirect(login_view)


def check_production(request, id):
    try:
        production = Production.objects.get(id=id, is_active=True)
        if production:
            if production.status == "cutting":
                production.is_cutting = True
                production.status = "polishing"
            elif production.status == "polishing":
                production.is_polishing = True
                production.status = "fabrication"
            elif production.status == "fabrication":
                production.is_fabrication = True
                production.status = "toughening"
            elif production.status == "toughening":
                production.is_toughening = True
                production.status = "dgu"
            elif production.status == "dgu":
                production.is_dgu = True
                production.status = "dispatch"
            else:
                production.status = "cutting"
            production.save()
    except ObjectDoesNotExist:
        production = None
    return redirect(production_view)


@login_required(login_url="/")
def inventory_view(request):
    if request.user.groups.filter(name__in=["Admin"]).exists():
        items = Item.objects.filter(in_stock__gt=0, is_active=True)
        context = {"items": items}
        return render(request, "inventory.html", context)
    else:
        return redirect(login_view)
