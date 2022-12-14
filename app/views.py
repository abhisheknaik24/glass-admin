from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from app.models import Cart, Feature, Item, Notification, Production, WorkOrder


def check_user(request, group):
    if request.user.is_authenticated:
        try:
            if request.user.groups.values_list() is not None:
                groups = list(request.user.groups.values_list("name", flat=True))
                if not group in groups:
                    return redirect(login_view)
        except Exception as e:
            raise e


def login_view(request):
    return render(request, "login.html")


@login_required(login_url="/")
def products_view(request):
    items = Item.objects.all()
    context = {"items": items}
    return render(request, "products.html", context)


@login_required(login_url="/")
def product_details_view(request, id):
    check_user(request, "Customer")
    try:
        item = Item.objects.get(id=id)
    except ObjectDoesNotExist:
        item = None
    features = Feature.objects.filter(item__id=id)
    context = {"item": item, "features": features}
    return render(request, "details.html", context)


@login_required(login_url="/")
def products_cart_view(request):
    check_user(request, "Customer")
    return render(request, "cart.html")


def add_to_cart(request, id):
    try:
        item = Item.objects.get(id=id)
        if item:
            cart_check = Cart.objects.filter(user=request.user.id, item=item).exists()
            if cart_check:
                cart = Cart.objects.get(user=request.user.id, item=item)
                cart.quantity += 1
                cart.save()
            else:
                cart = Cart(user=request.user.id, item=item, quantity=1)
                cart.save()
    except ObjectDoesNotExist:
        item = None
    return redirect(products_cart_view)


def increase_quantity(request, id):
    try:
        cart = Cart.objects.get(id=id, user=request.user.id)
        cart.quantity += 1
        cart.save()
    except ObjectDoesNotExist:
        cart = None
    return redirect(products_cart_view)


def decrease_quantity(request, id):
    try:
        cart = Cart.objects.get(id=id, user=request.user.id)
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
        cart = Cart.objects.get(id=id, user=request.user.id)
        cart.delete()
    except ObjectDoesNotExist:
        cart = None
    return redirect(products_cart_view)


def clear_cart(request):
    cart = Cart.objects.filter(user=request.user.id)
    cart.delete()
    return redirect(products_cart_view)


@login_required(login_url="/")
def products_checkout_view(request):
    check_user(request, "Customer")
    return render(request, "checkout.html")


@login_required(login_url="/")
def work_order_view(request):
    check_user(request, "Admin")
    return render(request, "work_order.html")


@login_required(login_url="/")
def cutting_view(request):
    check_user(request, "Admin")
    return render(request, "cutting.html")


@login_required(login_url="/")
def polishing_view(request):
    check_user(request, "Admin")
    return render(request, "polishing.html")


@login_required(login_url="/")
def fabrication_view(request):
    check_user(request, "Admin")
    return render(request, "fabrication.html")


@login_required(login_url="/")
def toughening_view(request):
    check_user(request, "Admin")
    return render(request, "toughening.html")


@login_required(login_url="/")
def dgu_view(request):
    check_user(request, "Admin")
    return render(request, "dgu.html")


@login_required(login_url="/")
def dispatch_view(request):
    check_user(request, "Admin")
    return render(request, "dispatch.html")


@login_required(login_url="/")
def inventory_view(request):
    check_user(request, "Admin")
    return render(request, "inventory.html")
