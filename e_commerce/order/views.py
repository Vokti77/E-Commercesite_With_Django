from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from order.models import Cart, Order

from coupon.forms import CouponCodeForm
from coupon.models import Coupon
from django.utils import timezone


def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)  # Current Product PK(id)
    orderitem = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)  # Cart and Order get or create objects with filer objects
    order_qs = Order.objects.filter(user=request.user, order=False)  # get order object //Tuples are not redirect

    if order_qs.exists():  # object indexing
        order = order_qs[0]
        if order.order_items.filter(item=item).exists():  # if product item exists
            size = request.POST.get('size')
            color = request.POST.get('color')
            quantity = request.POST.get('quantity')
            if quantity:
                orderitem[0].quantity += int(quantity)
            else:
                orderitem[0].quantity += 1   # quantity update
            orderitem[0].size = size
            orderitem[0].color = color
            orderitem[0].save()
            return redirect('/')
        else:
            order.order_items.add(orderitem[0])  # un-exists product item add to cart
            return redirect('/')
    else:
        order = Order(user=request.user)  # create new object
        size = request.POST.get('size')
        color = request.POST.get('color')
        orderitem[0].size = size
        orderitem[0].color = color
        order.save()
        order.order_items.add(orderitem[0])
        return redirect('/')


def cart_view(request):
    carts = Cart.objects.filter(user=request.user, purchased=False)
    orders = Order.objects.filter(user=request.user, order=False)
    if carts.exists() and orders.exists():
        order = orders[0]

        coupon_form = CouponCodeForm(request.POST)  # Coupon
        if coupon_form.is_valid():
            current_time = timezone.now()
            code = coupon_form.cleaned_data.get('code')
            coupon_obj = Coupon.objects.get(code=code, active=True)
            if coupon_obj.valid_to >= current_time:
                get_discount = (coupon_obj.discount/100) * order.get_totals()
                total_price_after_discount = order.get_totals() - get_discount
                request.session['discount_total'] = total_price_after_discount
                request.session['coupon_code'] = code
                return redirect('store:view-cart')
        total_price_after_discount = request.session.get('discount_total')
        coupon_code = request.session.get('coupon_code')
        context = {
            'carts': carts,
            'orders': orders,
            'coupon_form': coupon_form,
            'coupon_code': coupon_code,
            'total_price_after_discount': total_price_after_discount,
        }
        return render(request, 'store/cart.html', context)


def remove_item_from_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    orders = Order.objects.filter(user=request.user, order=False)
    if orders.exists():
        order = orders[0]
        if order.order_items.filter(item=item).exists():
            order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)
            order.order_items.remove(order_item[0])
            order_item.delete()
            return redirect('store:view-cart')
        else:
            return redirect('store:view-cart')
    else:
        return redirect('store:view-cart')

