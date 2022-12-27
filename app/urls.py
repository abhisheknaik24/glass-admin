from django.urls import path

from app import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("products/", views.products_view, name="products"),
    path("details/<int:id>/", views.product_details_view, name="details"),
    path("cart/", views.products_cart_view, name="cart"),
    path("add_to_cart/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "increase_quantity/<int:id>/", views.increase_quantity, name="increase_quantity"
    ),
    path(
        "decrease_quantity/<int:id>/", views.decrease_quantity, name="decrease_quantity"
    ),
    path("delete_cart/<int:id>/", views.delete_cart, name="delete_cart"),
    path("clear_cart/", views.clear_cart, name="clear_cart"),
    path("buy_now/<int:id>/", views.buy_now, name="buy_now"),
    path("checkout/", views.products_checkout_view, name="checkout"),
    path("work_order/", views.work_order_view, name="work_order"),
    path("add_work_order/", views.add_work_order, name="add_work_order"),
    path("production/", views.production_view, name="production"),
    path("inventory/", views.inventory_view, name="inventory"),
]
