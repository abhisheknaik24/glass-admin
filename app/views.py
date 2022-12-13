from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from app.models import Cart, Feature, Item, Notification


def login_view(request):
    return render(request, "login.html")


@login_required(login_url="/")
@permission_required(("app.can_view_item", "app.can_view_cart"), login_url="/")
def products_view(request):
    items = Item.objects.all()
    context = {"items": items}
    return render(request, "products.html", context)


def product_details_view(request, id):
    try:
        item = Item.objects.get(id=id)
    except ObjectDoesNotExist:
        item = None
    features = Feature.objects.filter(item__id=id)
    context = {"item": item, "features": features}
    return render(request, "details.html", context)


def products_cart_view(request):
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


def products_checkout_view(request):
    return render(request, "checkout.html")
