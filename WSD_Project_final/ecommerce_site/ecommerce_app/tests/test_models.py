from decimal import Decimal
from django.test import TestCase
from ecommerce_app.models import Product


class ProductModelTests(TestCase):
    def test_create_product(self):
        p = Product.objects.create(
            name="Test Dish",
            category="starters",
            price=Decimal("9.99"),
            image_name="test.jpg",
        )
        self.assertEqual(str(p), "Test Dish")
        self.assertEqual(p.category, "starters")
        self.assertGreater(p.price, 0)
