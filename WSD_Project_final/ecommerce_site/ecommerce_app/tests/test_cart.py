from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ecommerce_app.models import Product


class CartTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.product = Product.objects.create(
            name="Test Dish",
            category="starters",
            price=Decimal("5.00"),
            image_name="test.jpg",
        )

    def test_add_to_cart_session(self):
        self.client.login(username="testuser", password="testpass")
        resp = self.client.post(
            reverse("ecommerce_app:add_to_cart"),
            {"product_id": self.product.id, "quantity": 2},
        )
        self.assertEqual(resp.status_code, 302)  # redirect back to product

        session = self.client.session
        cart = session.get("cart", [])
        self.assertEqual(len(cart), 1)
        self.assertEqual(cart[0]["product_id"], self.product.id)
        self.assertEqual(cart[0]["quantity"], 2)
