from django.shortcuts import render
from stores.models import Product, ReviewRating, BannerGallery
from accounts.models import UserProfile
from currencies.models import Currency
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from store import settings


def home(request):
    title = 'Ernur Auto Emporium - Қозғалтқыштарға арналған түпнұсқа қосалқы бөлшектерді тікелей зауыттан сатушы.'
    
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

    product = Product.objects.filter(is_available=True).order_by('?')
    
    paginator = Paginator(product, 45)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    reviews_dict = {}
    for products in product:
        reviews_dict[products.id] = ReviewRating.objects.filter(product_id=products.id, status=True)

    banner = BannerGallery.objects.all()

    context = {
        'title': title,
        'product': paged_products,
        'reviews': reviews_dict, 
        'banner': banner,
        'currency': currency,  
    }
    
    return render(request, 'home.html', context)


def footer(request):
    product = Product.objects.all()
    context = {'product': product}
    return render(request, 'includes/footer.html', context)

@login_required(login_url='login')
def dashboard(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile_picture = user_profile.profile_picture if user_profile.profile_picture else static('images/default-profile.png')

    context = {
        'profile_picture': profile_picture,
    }

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
def savelangcur(request):
    lasturl = request.META.get('HTTP_REFERER')
    curren_user = request.user
    
    if 'currency' in request.session:
        user_profile, created = UserProfile.objects.get_or_create(user=curren_user)
        user_profile.currency_id = request.session['currency']
        user_profile.save()

    return HttpResponseRedirect(lasturl)


def selectcurrency(request):
    lasturl = request.META.get('HTTP_REFERER')
    
    if request.method == 'POST':  
        currency_code = request.POST.get('currency')
        if Currency.objects.filter(code=currency_code).exists(): 
            request.session['currency'] = currency_code
        else:
            request.session['currency'] = 'KZT'

    return HttpResponseRedirect(lasturl)