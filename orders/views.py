from django.shortcuts import render, redirect
from django.utils import timezone
from carts.models import CartItem
from orders.models import Order
from stores.models import Product
from django.contrib.auth.decorators import login_required

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

        # Сохраняем заказ
        order = Order()
        order.user = current_user
        order.аты_жөні = request.POST.get('аты_жөні')
        order.тегі = request.POST.get('тегі')
        order.электрондық_пошта = request.POST.get('email')
        order.phone = request.POST.get('phone')
        order.address_line_1 = request.POST.get('address_line_1')
        order.city = request.POST.get('city')
        order.country = request.POST.get('country')
        order.order_note = request.POST.get('order_note', '')
        order.tax = tax
        order.order_total = grand_total
        order.ip = request.META.get('REMOTE_ADDR')
        order.save()

        # Генерируем номер заказа
        date_str = timezone.now().strftime("%Y%m%d")
        order.order_number = f"{date_str}{order.id}"
        order.save()

        # Очищаем корзину
        cart_items.delete()

        # Переход на страницу подтверждения
        return render(request, 'orders/order_confirmation.html', {
            'order': order,
            'total': total,
            'tax': tax,
            'grand_total': grand_total,
        })

    return redirect('checkout')
