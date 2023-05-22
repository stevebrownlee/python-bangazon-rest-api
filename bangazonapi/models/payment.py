from django.db import models
from .customer import Customer

class Payment(models.Model):

    merchant_name = models.CharField(max_length=25,)
    account_number = models.CharField(max_length=25)
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="payment_types")
    expiration_date = models.DateField(default="0000-00-00",)
    create_date = models.DateField(default="0000-00-00",)

    class Meta:
        verbose_name = ("payment")
        verbose_name_plural = ("payments")
