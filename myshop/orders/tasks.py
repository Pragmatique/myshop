from celery import task
from django.core.mail import send_mail

from .models import Order, OrderItem
from shop.models import Product


from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q

@task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    print("Task completed")
    order = Order.objects.get(id=order_id)
    subject = 'Order nr. {}'.format(order.id)
    message = 'Dear {},\n\nYou have successfully placed an order.\
                  Your order id is {}.'.format(order.first_name,
                                            order.id)
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])




    return mail_sent


@task
def regular_delete_unconfirmed_preorders():

    print("Begin deleting")
    #updated > datetime.now() - timedelta(hours=5)
    time_threshold = datetime.now() - timedelta(minutes=5)
    unconfirmed_orders = Order.objects.filter(Q(updated__lt=time_threshold)&Q(status='NEW'))
    for order in unconfirmed_orders:
        order.status='EXPIRED'
        order.save()
        order_items=OrderItem.objects.filter(order=order)
        for order_item in order_items:
            product = order_item.product
            product.stock+=order_item.quantity
            product.save()
            order_item.quantity=0
            order_item.save()

