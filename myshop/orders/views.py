from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from decimal import Decimal
from django.db.models import Q
from datetime import datetime, timedelta, timezone

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from shop.models import Product
from .tasks import order_created

from authproj.models import User

# Create your views here.
def order_create(request):
    cart = Cart(request)
    if 'order_id' not in request.session:
        if request.method == 'POST' or request.user.is_authenticated==False:
            form = OrderCreateForm(request.POST)
            if form.is_valid() and cart.__len__()>0:
                order = form.save()
                if request.user.is_authenticated:
                    order.userid=request.user.id
                    order.save()

                for item in cart:
                    if int(item['quantity']) > int(item['product'].stock):
                        cart.add(product=item['product'],
                                 quantity=int(item['product'].stock),
                                 update_quantity=True,
                                 request=request)


                    OrderItem.objects.create(order=order,
                                            product=item['product'],
                                            price=item['price'],
                                            quantity=item['quantity']
                                             )

                    product = Product.objects.get(id=item['product'].id)
                    setattr(product,
                            'stock',
                            int(product.stock) - int(item['quantity'])
                            )
                    product.save()
                # clear the cart
                #cart.clear()
                # launch asynchronous task
                #print("Task completed")
                order_created.delay(order.id)
                # return render(request,
                #               'orders/order/created.html',
                #               {'orderid': order.id})
                # set the order in the session
                request.session['order_id'] = order.id
                # redirect for payment
                return redirect(reverse('payment:process'))

        else:
            form = OrderCreateForm( initial=
                                    {  'first_name':request.user.first_name,
                                       'last_name':request.user.last_name,
                                       'phone':request.user.phone,
                                       'email':request.user.email,
                                       'address':request.user.address,
                                       'city':request.user.city
                                    }
                                   )
    else:
        order = Order.objects.get(id=request.session['order_id'])
        ordered_items = order.items.all()
        for oritem in ordered_items:
            if int(oritem.quantity) > int(oritem.product.stock):
                cart.add(product=oritem.product,
                         quantity=oritem.product.stock,
                         update_quantity=True,
                         request=request)
                oritem.quantity=oritem.product.stock
                oritem.save()
                oritem.product.stock=0
                oritem.product.save()
                print(oritem.product)

        form = OrderCreateForm(request.POST or None,
                               instance=order,
                               initial=
                                {'first_name': request.user.first_name,
                                'last_name': request.user.last_name,
                                'phone': request.user.phone,
                                'email': request.user.email,
                                'address': request.user.address,
                                'city': request.user.city
                                }
                               )
        if form.is_valid():
            form.save()
            order_created.delay(order.id)
            #cart.clear()
            return redirect(reverse('payment:process'))



    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form}
                  )


def order_from_cart(request):

    cart = Cart(request)

    if request.user.is_authenticated:
        if 'order_id' not in request.session:
            order = Order.objects.create()
            order.status='NEW'
            order.userid=request.user.id
            order.first_name=request.user.first_name
            order.last_name=request.user.last_name
            order.address=request.user.address
            order.city=request.user.city
            order.email=request.user.email
            order.phone=request.user.phone
            order.save()
            print(request.session.keys())

            request.session['order_id']=order.id

            print(cart)
            print(request.session.keys())

            for item in cart:

                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity']
                                         )


                product = Product.objects.get(id=item['product'].id)
                setattr(product,
                        'stock',
                        int(Product.objects.get(id=item['product'].id).stock)-int(item['quantity'])
                        )
                product.save()

        else:
            order = Order.objects.get(id=request.session['order_id'])
            ordered_items=OrderItem.objects.filter(order=order)
            for oritem in ordered_items:
                print(oritem.product)

            for item in cart:

                if ordered_items.filter(product=item['product']).exists():

                    diff = int(item['quantity'])-int(ordered_items.get(product=item['product']).quantity)
                    order_item=ordered_items.get(product=item['product'])
                    order_item.quantity+=diff
                    order_item.save()

                    product = Product.objects.get(id=item['product'].id)
                    setattr(product,
                            'stock',
                            int(Product.objects.get(id=item['product'].id).stock) - diff
                            )
                    product.save()
                else:
                    OrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity']
                                             )

                    product = Product.objects.get(id=item['product'].id)
                    setattr(product,
                            'stock',
                            int(Product.objects.get(id=item['product'].id).stock) - int(item['quantity'])
                            )
                    product.save()

def del_from_preorder(request,product):
    if 'order_id' in request.session:
        cart = Cart(request)
        order = Order.objects.get(id=request.session['order_id'])

        product = product
        ordered_item = OrderItem.objects.get(Q(order=order) & Q(product=product))
        quantity=int(ordered_item.quantity)
        setattr(product,
                'stock',
                int(product.stock) + int(quantity)
                )
        product.save()

        ordered_item.quantity=0
        ordered_item.save()
