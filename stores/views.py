from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ReviewRating, ProductGallery
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from orders.models import OrderProduct
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import ReviewForm, ContactForm
from django.core.mail import EmailMessage, BadHeaderError
from django.conf import settings



def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug:
        categories = get_object_or_404(Category, url=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 6)
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products, 30)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    product_count = products.count()
    context = {'product': paged_products, 'product_count': product_count}
    return render(request, 'store/store.html', context)

def product_details(request, category_slug, product_slug):
    single_product = get_object_or_404(Product, category__url=category_slug, slug=product_slug)
    if_in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    order_product = OrderProduct.objects.filter(user=request.user, product=single_product).exists() if request.user.is_authenticated else None
    reviews = ReviewRating.objects.filter(product=single_product, status=True)
    product_gallery = ProductGallery.objects.filter(product=single_product)
    context = {
        'single_product': single_product,
        'if_in_cart': if_in_cart,
        'order_product': order_product,
        'reviews': reviews,
        'product_gallery': product_gallery
    }
    return render(request, 'store/product_details.html', context)

def search(request):
    if 'my-search' in request.GET:  # If my-search which is input name=search is in the url; store it in the variable my-search
        my_search = request.GET['my-search']
        if my_search:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=my_search) | Q(product_name__icontains=my_search))
            product_count = products.count()
        context = {
            'product': products,
            'product_count': product_count,
        }
        return render(request, 'store/store.html', context)


@login_required(login_url='login')
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')  # Для возврата на ту же страницу
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            # Если отзыв уже существует — обновим его
            existing_review = ReviewRating.objects.get(user=request.user, product=product)
            form = ReviewForm(request.POST, instance=existing_review)
            if form.is_valid():
                updated_review = form.save(commit=False)
                updated_review.ip = request.META.get('REMOTE_ADDR')
                updated_review.status = True  # ВАЖНО: показывать на странице
                updated_review.save()
                messages.success(request, 'Сіздің пікіріңіз жаңартылды.')
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                new_review = ReviewRating(
                    subject=form.cleaned_data['subject'],
                    review=form.cleaned_data['review'],
                    rating=form.cleaned_data['rating'],
                    ip=request.META.get('REMOTE_ADDR'),
                    product=product,
                    user=request.user,
                    status=True  # ВАЖНО: показывать на странице
                )
                new_review.save()
                messages.success(request, 'Сіздің пікіріңіз сәтті жіберілді.')
            else:
                messages.error(request, 'Формада қате бар.')

    return redirect(url)


def terms(request):
    title = "Ережелер мен шарттар"
    context = {'title': title}
    return render(request, 'store/terms.html', context)


def delivery(request):
    title = "Ережелер мен шарттар"
    context = {'title': title}
    return render(request, 'store/delivery.html', context)


def refund(request):
    title = "Ережелер мен шарттар"
    context = {'title': title}
    return render(request, 'store/refund.html', context)


def privacy(request):
    title = "Ережелер мен шарттар"
    context = {'title': title}
    return render(request, 'store/privacy.html', context)


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_email = EmailMessage(subject=subject, body=message, from_email=email, to=['support@ernurautoemporium.com'])
                send_email.send()
                messages.success(request, 'Сіздің хабарламаңыз жіберілді!')
            except BadHeaderError:
                return HttpResponse('Жарамсыз тақырып табылды.')
            return redirect('home')
    return render(request, "store/contact.html", {'form': form})

def home(request):
    return render(request, 'home.html')

def selectcurrency(request):
    return HttpResponse("Currency selection placeholder")

from django.http import JsonResponse

def savelangcur(request):
    # Заглушка: ничего не делает, но возвращает успешный ответ
    return JsonResponse({'status': 'ok'})
