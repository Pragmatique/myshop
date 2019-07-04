from datetime import datetime, timedelta

from django.db import models
from shop.models import Product

# Create your models here.
ORDER_STATUSES=(
    ('NEW', "NEW"),
    ('CONFIRMED', "CONFIRMED"),
    ('EXPIRED', "EXPIRED"),
)

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    userid=models.IntegerField(null=True,default=None)
    status = models.CharField(max_length=150, blank=True, choices=ORDER_STATUSES, default=ORDER_STATUSES[0][0])
    #expire_at = models.DateTimeField(blank=True, default=datetime.now()+timedelta(minutes=30))

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity