from django.shortcuts import render

from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created

from authproj.models import User

# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST' or request.user.is_authenticated==False:
        form = OrderCreateForm(request.POST)
        if form.is_valid() and cart.__len__()>0:
            order = form.save()
            if request.user.is_authenticated:
                order.userid=request.user.id
                order.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity']
                                         )
            # clear the cart
            cart.clear()
            # launch asynchronous task
            #print("Task completed")
            order_created.delay(order.id)
            return render(request,
                          'orders/order/created.html',
                          {'orderid': order.id})

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
        # form.fields['first_name']=User.objects.get(user=request.user).first_name
        # form.fields['last_name'] = User.objects.get(user=request.user).last_name
        # form.fields['phone'] = User.objects.get(user=request.user).phone
        # form.fields['email'] = User.objects.get(user=request.user).email
        # form.fields['address'] = User.objects.get(user=request.user).address
        # form.fields['city'] = User.objects.get(user=request.user).city



    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})