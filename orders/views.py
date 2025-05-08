from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from carts.models import CartItem
from orders.models import Order, OrderProduct
from django.contrib import admin
from stores.models import Product, ReviewRating
from .forms import ReviewForm

@login_required(login_url='login')
def place_order(request):
    if request.method == 'POST':
        current_user = request.user
        cart_items = CartItem.objects.filter(user=current_user)

        if not cart_items.exists():
            return redirect('store')

        total = 0
        quantity = 0
        for item in cart_items:
            total += item.product.price * item.quantity
            quantity += item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

        # Create the order
        order = Order(
            user=current_user,
            аты_жөні=request.POST.get('аты_жөні'),
            тегі=request.POST.get('тегі'),
            электрондық_пошта=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address_line_1=request.POST.get('address_line_1'),
            city=request.POST.get('city'),
            country=request.POST.get('country'),
            order_note=request.POST.get('order_note', ''),
            tax=tax,
            order_total=grand_total,
            ip=request.META.get('REMOTE_ADDR'),
            is_ordered=True,
        )
        order.save()
        order.order_number = timezone.now().strftime("%Y%m%d") + str(order.id)
        order.save()

        # Create ordered products
        for item in cart_items:
            order_product = OrderProduct.objects.create(
                order=order,
                user=current_user,
                product=item.product,
                quantity=item.quantity,
                product_price=item.product.price,
                ordered=True
            )
            if item.variations.exists():
                order_product.variations.set(item.variations.all())

        cart_items.delete()

        return render(request, 'orders/order_confirmation.html', {
            'order': order,
            'total': total,
            'tax': tax,
            'grand_total': grand_total,
        })

    return redirect('checkout')


@login_required(login_url='login')
def submit_review(request, order_product_id):
    order_product = get_object_or_404(OrderProduct, id=order_product_id, user=request.user)
    product = order_product.product

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.ip = request.META.get('REMOTE_ADDR')
            review.status = True
            review.save()

            order_product.is_rated = True
            order_product.save()

            messages.success(request, 'Пікіріңіз сәтті сақталды.')
            return redirect('product_details', category_slug=product.category.slug, product_slug=product.slug)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'product_review': order_product,
        'product': product,
    }
    return render(request, 'orders/submit_review.html', context)