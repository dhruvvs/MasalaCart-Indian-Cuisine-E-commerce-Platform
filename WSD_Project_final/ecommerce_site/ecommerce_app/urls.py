from django.urls import path, include
from . import views

app_name = "ecommerce_app"

urlpatterns = [
    # Orders
    path("place_order/", views.place_order, name="place_order"),
    path("my_orders/", views.my_orders, name="my_orders"),

    # Auth
    path("signup.html", views.authView, name="authView"),
    path("logout.html", views.logout_view, name="logmeout"),
    path("accounts/", include("django.contrib.auth.urls")),

    # Core pages
    path("", views.product, name="product"),
    path("cartDetails.html", views.cartDetails, name="cartDetails"),
    path("thankYou.html", views.thankYou, name="thankYou"),

    # Cart actions
    path("add-to-cart", views.add_to_cart, name="add_to_cart"),
    path("update_cart/", views.update_cart, name="update_cart"),
    
    path("orders/<int:order_id>/reorder/", views.reorder_order, name="reorder_order"),
]
from . import views

app_name = "ecommerce_app"

urlpatterns = [
    # Orders
    path("place_order/", views.place_order, name="place_order"),
    path("my_orders/", views.my_orders, name="my_orders"),

    # Auth
    path("signup.html", views.authView, name="authView"),
    path("logout.html", views.logout_view, name="logmeout"),
    path("accounts/", include("django.contrib.auth.urls")),

    # Core pages
    path("", views.product, name="product"),
    path("cartDetails.html", views.cartDetails, name="cartDetails"),
    path("thankYou.html", views.thankYou, name="thankYou"),

    # Cart actions
    path("add-to-cart", views.add_to_cart, name="add_to_cart"),
    path("update_cart/", views.update_cart, name="update_cart"),

    # --- API endpoints ---
    path("api/products/", views.api_products, name="api_products"),
    path("api/cart/", views.api_cart, name="api_cart"),
    path("orders/<int:order_id>/reorder/", views.reorder_order, name="reorder_order"),
]
