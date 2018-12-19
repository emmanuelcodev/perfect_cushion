from django.shortcuts import render
from shop.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
#from order.models import Order, OrderItem
#from django.template.loader import get_template
#from django.core.mail import EmailMessage
# Create your views here.


def _cart_id(request):#all about session
    cart = request.session.session_key#checks if there is a session key in the browser
    print('cart session key is', cart)
    if not cart:
        cart = request.session.create()
        print('cart session after being made is', cart)
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=(_cart_id(request)))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = (_cart_id(request)))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart = cart)
        cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product = product, quantity = 1, cart = cart)
        cart_item.save()

    return redirect('cart:cart_detail')



def cart_detail(request, total=0, counter = 0, cart_items = None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return (request, 'cart.html', dict(cart_items = cart_items, total = total, counter = counter))
