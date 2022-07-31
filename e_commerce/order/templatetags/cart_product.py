from django import template
from order.models import Cart, Order

register = template.Library()


@register.filter
def cart_view(user):
    cart = Cart.objects.filter(user=user, purchased=False)
    if cart.exists():
        return cart
    else:
        return cart
        # return ValueError("You have not active your cart!")


@register.filter
def cart_total(user):
    odered = Order.objects.filter(user=user, order=False)
    if odered.exists():
        return odered[0].get_totals()
    else:
        return 0


@register.filter
def order_count(user):
    ordered = Order.objects.filter(user=user, order=False)
    if ordered.exists():
        return ordered[0].order_items.count()
    else:
        return 0