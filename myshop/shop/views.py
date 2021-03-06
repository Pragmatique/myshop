from django.shortcuts import render
from datetime import datetime, timedelta, timezone
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from .models import Category, Product

from cart.forms import CartAddProductForm

# Create your views here.
def product_list(request, category_slug=None):

    #print(datetime.now(timezone.utc) - timedelta(minutes=5))

    #user_language = request.LANGUAGE_CODE
    #translation.activate(user_language)

    # user_language='en'
    # translation.activate(user_language)
    # request.session[translation.LANGUAGE_SESSION_KEY]=user_language

    # if translation.LANGUAGE_SESSION_KEY in request.session[translation.LANGUAGE_SESSION_KEY]:
    #     del request.session[translation.LANGUAGE_SESSION_KEY]

    category = None
    categories = Category.objects.all()
    for categor in categories:
        categor.name = _(categor.name)

    products = Product.objects.filter(available=True)
    for product in products:
        product.name = _(product.name)
        product.description = _(product.description)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        #language = request.LANGUAGE_CODE
        # code for translated slug
        # category = get_object_or_404(Category,
        #                              translations__language_code=language
        #                              ,translations__slug=category_slug
        #                              )
        #category.name=_(category.name)

        products = products.filter(category=category)
        for product in products:
            product.name = _(product.name)
            product.description = _(product.description)



            #product.category=_(product.category)



    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    product.name = _(product.name)
    product.description = _(product.description)

    #print(request.session.keys())


    max_stock = Product.objects.get(id=id).stock
    #print(max_stock)
    #max_stock=None
    #cart_product_form = CartAddProductForm(request,max_stock)
    #cart_product_form = CartAddProductForm(request.POST)
    cart_product_form = CartAddProductForm(max_stock=max_stock)
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


