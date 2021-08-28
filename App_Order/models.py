from django.db import models
from django.conf import settings
# Create your models here.
from App_Shop.models import Food
class Cart(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="cart")
    item=models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    purchased=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quantity} X {self.item}'
    def get_total(self):
        total=self.item.price * self.quantity
        float_total= format(total, '0.2f')
        return float_total
    def get_orders(self):
        return self.item
class Order(models.Model):
    orderitems=models.ManyToManyField(Cart)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    order_done=models.BooleanField(default=False)
    order_to_review=models.IntegerField(default=0)
    paymentId=models.CharField(max_length=264, blank=True, null=True)
    orderId=models.CharField(max_length=200, blank=True, null=True)

    def get_totals(self):
        total=0
        for order_item in self.orderitems.all():
            total +=float(order_item.get_total())
        return total
