from django.db import models
from django.conf import settings
from App_Shop.models import Food
from App_Order.models import Order
# Create your models here.

class Review_Cart(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="review_user")
    item=models.ForeignKey(Food, on_delete=models.CASCADE)
    reviewed_food=models.BooleanField(default=False)
    admin_check=models.BooleanField(default=False)
    review_food=models.TextField(max_length=1000, verbose_name="Review",null=True)
    rate=(
    (1,"Worst"),
    (2,"Not Bad"),
    (3,"Good"),
    (4,"Better"),
    (5,"Delicious")
    )
    rating=models.IntegerField(choices=rate,null=True)

    def __str__(self):
        return f'{self.item}'

class Review(models.Model):
    orderitems=models.ManyToManyField(Review_Cart)
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    reviewed=models.BooleanField(default=False)
    review_order=models.TextField(max_length=1000, verbose_name="Review Order",blank=True, null=True)
