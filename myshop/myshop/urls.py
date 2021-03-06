"""myshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include(('django.conf.urls.i18n','i18n'), namespace='i18n')),

    ]
urlpatterns+=i18n_patterns(
    url(r'^cart/', include(('cart.urls','cart'), namespace='cart')),
    url(r'^orders/', include(('orders.urls','orders'), namespace='orders')),
    url(r'^auth/', include(('authproj.urls','authproj'), namespace='authproj')),
    url(r'^paypal/', include(('paypal.standard.ipn.urls','paypal.standard.ipn'), namespace='paypal.standard.ipn')),
    url(r'^payment/', include(('payment.urls','payment'), namespace='payment')),
    url(r'^', include(('shop.urls','shop'), namespace='shop')),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
