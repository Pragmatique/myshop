from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from paypal.standard.forms import PayPalPaymentsForm
from orders.models import Order
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host=request.get_host()

    paypal_dict = {
        'business':settings.PAYPAL_RECEIVER_EMAIL,
        'amount':'%.2f'%order.get_total_cost().quantize(Decimal('.01')),
        'item_name':'Order {}'.format(order.id),
        'invoice':str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,reverse('paypal.standard.ipn:paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),

    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    # form=None

    return render(request,'payment/process.html',{'order':order,'form':form})

    # if request.method == 'POST':
    #     # retrieve nonce
    #     nonce = request.POST.get('payment_method_nonce', None)
    #     # create and submit transaction
    #     result = braintree.Transaction.sale({
    #         'amount': '{:.2f}'.format(order.get_total_cost()),
    #         'payment_method_nonce': nonce,
    #         'options': {
    #             'submit_for_settlement': True
    #             }
    #     })
    #     if result.is_success:
    #         # mark the order as paid
    #         order.paid = True
    #         # store the unique transaction id
    #         order.braintree_id = result.transaction.id
    #         order.save()
    #         return redirect('payment:done')
    #     else:
    #         return redirect('payment:canceled')
    # else:
    #     # generate token
    #     client_token = braintree.ClientToken.generate()
    #     return render(request,
    #                     'payment/process.html',
    #                     {'order': order,
    #                     'client_token': client_token})

@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
