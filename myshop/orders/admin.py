from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product','order']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'phone', 'city', 'paid',
                    'created', 'updated', 'userid']
    list_filter = ['paid', 'created', 'updated','status']
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)