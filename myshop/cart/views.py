from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _

from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from orders.views import order_from_cart, del_from_preorder
# Create your views here.


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    max_stock = Product.objects.get(id=product_id).stock
    form = CartAddProductForm(max_stock=max_stock,data=request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'],
                 request=request)
        order_from_cart(request)
        # for key, value in request.session.items():
        #     print('{} => {}'.format(key, value))


    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    del_from_preorder(request, product)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    print(cart.cart.keys())
    for item in cart:
        #print(_(item['product'].name))
        #item['product'].name=_(item['product'].name)
        max_stock = Product.objects.get(id=item['product'].id).stock
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True}, max_stock=max_stock)
        #print(item['product'].name)


    return render(request, 'cart/detail.html', {'cart': cart})