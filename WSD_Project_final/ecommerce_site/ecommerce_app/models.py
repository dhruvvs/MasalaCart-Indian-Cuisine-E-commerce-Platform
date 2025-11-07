from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('starters', 'Starters'),
        ('main_course', 'Main Course'),
        ('desserts', 'Desserts'),
        ('beverages', 'Beverages'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_name = models.CharField(max_length=100)  # This should match the image filename in static/images/

    def __str__(self):
        return self.name
