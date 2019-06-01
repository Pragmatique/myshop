from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _

from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
# Create your views here.


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    #product.name=_(product.name)
    print(request.session)
    #max_stock=request.session.products.get(id=product_id)['stock']
    max_stock=None
    form = CartAddProductForm(request.POST,max_stock)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    print(cart.cart)
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    #print(cart.cart.keys())
    for item in cart:
        #print(_(item['product'].name))
        #item['product'].name=_(item['product'].name)
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'update': True})
        #print(item['product'].name)


    return render(request, 'cart/detail.html', {'cart': cart})