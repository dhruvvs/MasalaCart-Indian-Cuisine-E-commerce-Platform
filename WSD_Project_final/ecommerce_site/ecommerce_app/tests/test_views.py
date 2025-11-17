from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ecommerce_app.models import Product


class ProductViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.product = Product.objects.create(
            name="Paneer Tikka",
            category="starters",
            price=Decimal("10.00"),
            image_name="paneer.jpg",
        )

    def test_product_page_renders(self):
        self.client.login(username="testuser", password="testpass")
        resp = self.client.get(reverse("ecommerce_app:product"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Paneer Tikka")
