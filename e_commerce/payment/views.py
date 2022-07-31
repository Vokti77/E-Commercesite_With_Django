from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from payment.models import BillingAddress
from payment.forms import BillingAddressForm, PaymentMethodForm
from order.models import Cart, Order

from django.views.generic import TemplateView


class CheckoutTemplateView(TemplateView):
    def get(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
        saved_address = saved_address[0]
        form = BillingAddressForm(instance=saved_address)
        payment_method = PaymentMethodForm
        oder_qs = Order.objects.filter(user=request.user, order=False)
        orderitems = oder_qs[0].order_items.all()
        order_total = oder_qs[0].get_totals()
        context = {
            'billing_address': form,
            'orderitems': orderitems,
            'order_total': order_total,
            'payment_method': payment_method,
        }
        return render(request, 'store/checkout.html', context)

    def post(self, request, *args, **kwargs):
        saved_address = BillingAddress.objects.get_or_create(user=request.user or None)
        saved_address = saved_address[0]
        form = BillingAddressForm(instance=saved_address)
        payment_obj = Order.objects.filter(user=request.user, order=False)[0]
        payment_form = PaymentMethodForm(instance=payment_obj)
        if request.method == 'post' or request.method == 'POST':
            form = BillingAddressForm(request.POST, instance=saved_address)
            pay_form = PaymentMethodForm(request.POST, instance=payment_obj)
            if form.is_valid() and pay_form.is_valid():
                form.save()
                pay_method = pay_form.save()
                # return redirect('store:view-cart')
                if not saved_address.is_fully_filled():
                    return redirect('checkout')

                # Cash on Delivery method process
                if pay_method.payment_method == 'Cash on Delivery':
                    order_qs = Order.objects.filter(user=request.user, order=False)
                    order = order_qs[0]
                    order.order = True
                    order.order_Id = order.id
                    order.payment_Id = pay_method.payment_method
                    order.save()
                    cart_items = Cart.objects.filter(user=request.user, purchased=False)
                    for item in cart_items:
                        item.purchased = True
                        item.save()
                    print("Order Submitted Successfully!")
                    return redirect('/')



