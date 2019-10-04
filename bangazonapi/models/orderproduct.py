from django.db import models
from .order import Order
from .product import Product

class OrderProduct(models.Model):

    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING,)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING,)
    quantity = models.IntegerField()

    class Meta:
        verbose_name = ("orderproduct")
        verbose_name_plural = ("orderproducts")