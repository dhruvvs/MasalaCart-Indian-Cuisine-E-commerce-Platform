from decimal import Decimal

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Product, Order, OrderItem, Address
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import F


from .serializers import ProductSerializer


from django.urls import reverse



# ---------- Cart helper ----------

def build_cart_context(request):
    """
    Reads cart from session and returns:
    - cart_items: list of dicts {product, quantity, line_total}
    - total_quantity
    - total_price (Decimal)
    """
    cart = request.session.get("cart", [])
    cart_items = []
    total_quantity = 0
    total_price = Decimal("0.00")

    for item in cart:
        product = get_object_or_404(Product, pk=item["product_id"])
        quantity = int(item["quantity"])
        if quantity <= 0:
            continue

        line_total = product.price * quantity

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "line_total": line_total,
            }
        )
        total_quantity += quantity
        total_price += line_total

    return cart_items, total_quantity, total_price


# ---------- Core pages ----------

from django.core.paginator import Paginator  # already imported in your file

@login_required
def product(request):
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    products_qs = Product.objects.all()

    if q:
        products_qs = products_qs.filter(name__icontains=q)

    if category:
        products_qs = products_qs.filter(category=category)

    paginator = Paginator(products_qs, 9)  # 9 products per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Cart info for navbar
    cart_items, total_quantity, total_price = build_cart_context(request)

    context = {
        "products": page_obj.object_list,   # for your existing loop
        "page_obj": page_obj,               # for pagination controls
        "q": q,
        "selected_category": category,
        "total_cart_quantity": total_quantity,
        "cart_count": total_quantity,
        "cart_total": total_price,
    }

    popular_products = Product.objects.order_by("-times_added_to_cart")[:4]

    context = {
        "products": page_obj.object_list,
        "page_obj": page_obj,
        "q": q,
        "selected_category": category,
        "total_cart_quantity": total_quantity,
        "cart_count": total_quantity,
        "cart_total": total_price,
        "popular_products": popular_products,
    }
    return render(request, "Product.html", context)



@login_required
def cartDetails(request):
    cart_items, total_quantity, total_price = build_cart_context(request)
    cart_empty = len(cart_items) == 0

    # Try to load saved address for this user
    address = None
    try:
        address = request.user.address
    except Address.DoesNotExist:
        address = None

    # Optional: keep totals in session (not needed for thankYou anymore,
    # but might be useful elsewhere)
    request.session["total_quantity"] = total_quantity
    request.session["total_price"] = float(total_price)

    context = {
        "cart_items": cart_items,
        "total_quantity": total_quantity,
        "total_price": total_price,
        "cart_empty": cart_empty,
        "address": address,
    }
    return render(request, "cartDetails.html", context)


@login_required
def thankYou(request):
    order_id = request.session.get("last_order_id")
    order = None

    if order_id:
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            order = None

    context = {
        "order": order,
    }
    return render(request, "thankYou.html", context)


# ---------- Auth ----------

def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Django auth login URL from contrib.auth.urls
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return render(request, "logout.html")


# ---------- Cart actions ----------



@login_required
def update_cart(request):
    if request.method == "POST":
        product_id = int(request.POST.get("product_id"))
        quantity_change = int(request.POST.get("quantity"))

        cart = request.session.get("cart", [])
        for item in cart:
            if item["product_id"] == product_id:
                item["quantity"] += quantity_change
                if item["quantity"] < 1:
                    cart.remove(item)
                break

        request.session["cart"] = cart

        # ✅ if user clicked "+", treat it as "added to cart"
        if quantity_change > 0:
            Product.objects.filter(id=product_id).update(
                times_added_to_cart=F("times_added_to_cart") + quantity_change
            )


    return redirect("ecommerce_app:cartDetails")


# ---------- Orders ----------

@login_required
def place_order(request):
    # Only allow POST from the checkout form
    if request.method != "POST":
        return redirect("ecommerce_app:cartDetails")

    cart = request.session.get("cart", [])
    if not cart:
        return redirect("ecommerce_app:cartDetails")

    cart_items, total_quantity, total_price = build_cart_context(request)
    if not cart_items:
        return redirect("ecommerce_app:cartDetails")
    
    # 👉 Read shipping data from the form
    full_name = request.POST.get("full_name", "").strip()
    phone = request.POST.get("phone", "").strip()
    street = request.POST.get("street", "").strip()
    city = request.POST.get("city", "").strip()
    state = request.POST.get("state", "").strip()
    zip_code = request.POST.get("zip_code", "").strip()

    # Save/Update address profile for user
    if full_name and street and city and zip_code:
        Address.objects.update_or_create(
            user=request.user,
            defaults={
                "full_name": full_name,
                "phone": phone,
                "street": street,
                "city": city,
                "state": state,
                "zip_code": zip_code,
            },
        )


    # Create main Order
    order = Order.objects.create(
        user=request.user,
        total_quantity=total_quantity,
        total_price=total_price,
        status="PENDING",
        full_name=full_name,
        phone=phone,
        street=street,
        city=city,
        state=state,
        zip_code=zip_code,
    )

    # Create OrderItems
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item["product"],
            quantity=item["quantity"],
            price_at_purchase=item["product"].price,
        )

    # Clear cart
    request.session["cart"] = []
    request.session.modified = True

    # Remember last order for thankYou page
    request.session["last_order_id"] = order.id

    return redirect("ecommerce_app:thankYou")


@login_required
def my_orders(request):
    orders = (
        Order.objects.filter(user=request.user)
        .order_by("-created_at")
        .prefetch_related("items__product")
    )
    return render(request, "my_orders.html", {"orders": orders})
@login_required
def reorder_order(request, order_id):
    """
    Replace current cart with all items from a past order,
    then send user to cart page.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    new_cart = []
    for item in order.items.select_related("product"):
        product = item.product
        new_cart.append(
            {
                "product_id": product.id,
                "quantity": item.quantity,
                "name": product.name,
                "price": str(item.price_at_purchase),  # price at that time
                "image_name": product.image_name,
            }
        )

    request.session["cart"] = new_cart
    request.session.modified = True

    return redirect("ecommerce_app:cartDetails")


@api_view(["GET"])
def api_products(request):
    """
    JSON list of products with optional ?q= and ?category= filters.
    """
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    products = Product.objects.all()

    if q:
        products = products.filter(name__icontains=q)
    if category:
        products = products.filter(category=category)

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def api_cart(request):
    """
    Returns current session cart as JSON using build_cart_context.
    """
    cart_items, total_quantity, total_price = build_cart_context(request)

    data = {
        "items": [
            {
                "product_id": item["product"].id,
                "name": item["product"].name,
                "category": item["product"].category,
                "price": str(item["product"].price),
                "quantity": item["quantity"],
                "line_total": str(item["line_total"]),
            }
            for item in cart_items
        ],
        "total_quantity": total_quantity,
        "total_price": str(total_price),
    }
    return Response(data)

@login_required
def add_to_cart(request):
    if request.method == "POST":
        product_id = int(request.POST.get("product_id"))
        quantity = int(request.POST.get("quantity", 0))

        if quantity < 1:
            return redirect("ecommerce_app:product")

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect("ecommerce_app:product")

        cart = request.session.get("cart", [])

        # update session cart
        for item in cart:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                break
        else:
            cart.append(
                {
                    "product_id": product.id,
                    "quantity": quantity,
                    "name": product.name,
                    "price": str(product.price),
                    "image_name": product.image_name,
                }
            )

        request.session["cart"] = cart

        # 🔥 increment popularity (by quantity)
        Product.objects.filter(id=product.id).update(
            times_added_to_cart=F("times_added_to_cart") + quantity
        )

    return redirect("ecommerce_app:product")


