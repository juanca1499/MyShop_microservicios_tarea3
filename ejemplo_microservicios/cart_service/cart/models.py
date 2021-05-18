from django.db import models

class Cart(models.Model):
    session_id = models.CharField(max_length=10)
    total = models.DecimalField(max_digits=15, decimal_places=2)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    image = models.ImageField(blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=11, decimal_places=2)