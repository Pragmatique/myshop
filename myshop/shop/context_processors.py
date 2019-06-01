from .models import Product

def products(request):
    products = Product.objects.filter(available=True)
    return {'availible_products': products}