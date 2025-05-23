from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from stores.models import Product, Variation
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from currencies.models import Currency


def cart(request):
    if not request.session.get('currency'):
        currency = Currency.objects.filter(code="KZT").first()
        if not currency:
            request.session['currency'] = 'KZT'
        else:
            request.session['currency'] = currency.code

    currency_code = request.session.get('currency', 'KZT')
    currency = Currency.objects.filter(code=currency_code).first()

    if not currency:
        currency = Currency.objects.filter(code="KZT").first()
        request.session['currency'] = 'KZT'

    cart_items = Cart.objects.filter(user=request.user)  
    total = sum([item.quantity * item.product.price for item in cart_items])
    tax = total * 0.12 
    grand_total = total + tax

    context = {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
        'currency': currency, 
    }

    return render(request, 'cart.html', context)

def _cart_id(request):
    cart = request.session.session_key  
    if not cart:
        cart = request.session.create() 
    return cart

@csrf_exempt
def add_to_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    product_variation = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass

    if current_user.is_authenticated:
        cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            existing_variation_list, id_list = [], []

            for item in cart_item:
                existing_variation_list.append(list(item.variations.all()))
                id_list.append(item.id)

            if product_variation in existing_variation_list:
                index = existing_variation_list.index(product_variation)
                item_id = id_list[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                new_cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    new_cart_item.variations.clear()
                    new_cart_item.variations.add(*product_variation)
                new_cart_item.save()
        else:
            new_cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
            if len(product_variation) > 0:
                new_cart_item.variations.clear()
                new_cart_item.variations.add(*product_variation)
            new_cart_item.save()

        return redirect('cart')

    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            existing_variation_list, id_list = [], []

            for item in cart_item:
                existing_variation_list.append(list(item.variations.all()))
                id_list.append(item.id)

            if product_variation in existing_variation_list:
                index = existing_variation_list.index(product_variation)
                item_id = id_list[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                new_cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    new_cart_item.variations.clear()
                    new_cart_item.variations.add(*product_variation)
                new_cart_item.save()
        else:
            new_cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                new_cart_item.variations.clear()
                new_cart_item.variations.add(*product_variation)
            new_cart_item.save()

        return redirect('cart')

def remove_or_delete(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def delete_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
    except:
        pass
    return redirect('cart')

def cart(request, tax=0, grand_total=0, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)

@login_required(login_url='login')
def checkout(request, tax=0, grand_total=0, total=0, quantity=0, cart_items=None):
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)
