from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from django.templatetags.static import static
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from carts.views import _cart_id
from carts.models import Cart, CartItem
from orders.models import Order, OrderProduct
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect
from accounts.models import Account
import requests

def demo_login(request):
    if request.user.is_authenticated:
        return redirect('/admin/')  # если уже вошёл

    try:
        demo_user = Account.objects.get(электрондық_пошта="admin06ernur@mail.ru")
        demo_user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, demo_user)
        return redirect('/admin/')
    except Account.DoesNotExist:
        return HttpResponse("❌ Demo user not found", status=404)

def load_superuser(request):
    return HttpResponse("🔒 Superuser load disabled in production.")
    
def debug_users(request):
    users = Account.objects.values('электрондық_пошта', 'is_staff', 'is_superuser', 'is_active')
    return JsonResponse(list(users), safe=False)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            аты_жөні = form.cleaned_data['аты_жөні']
            тегі = form.cleaned_data['тегі']
            телефон_нөмірі = form.cleaned_data['телефон_нөмірі']
            электрондық_пошта = form.cleaned_data['электрондық_пошта']
            password = form.cleaned_data['password']
            username = электрондық_пошта.split('@')[0]

            user = Account.objects.create_user(
                аты_жөні=аты_жөні,
                тегі=тегі,
                электрондық_пошта=электрондық_пошта,
                username=username,
                password=password
            )
            user.телефон_нөмірі = телефон_нөмірі
            user.is_active = False  # Аккаунт активируется только через email
            user.save()

            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = static('images/default-profile.png')
            profile.save()

            current_site = get_current_site(request)
            mail_subject = 'Тіркелгіңізді белсендіріңіз'
            message = render_to_string('accounts/verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = электрондық_пошта
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&email=' + электрондық_пошта)
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        электрондық_пошта = request.POST['email']
        password = request.POST['password']

        try:
            user_check = Account.objects.get(электрондық_пошта=электрондық_пошта)
        except Account.DoesNotExist:
            messages.error(request, 'Бұл электрондық пошта тіркелмеген')
            return redirect('login')

        user = auth.authenticate(request, username=электрондық_пошта, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                messages.success(request, 'Сіз енді жүйеге кірдіңіз')
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
            else:
                messages.error(request, 'Аккаунт әлі белсендірілмеген. Электрондық поштаңызды тексеріңіз.')
                return redirect('login')
        else:
            messages.error(request, 'Қате email немесе құпия сөз')
            return redirect('login')

    return render(request, 'accounts/login.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Құттықтаймыз, тіркелгіңіз іске қосылды!')
        return redirect('login')
    else:
        messages.error(request, 'Жарамсыз белсендіру сілтемесі')
        return redirect('register')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Жүйеден сәтті шықты')
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    order_count = orders.count()

    context = {
        'profile_picture': user_profile.profile_picture,
        'order_count': order_count,
    }

    return render(request, 'accounts/dashboard.html', context)


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(электрондық_пошта=email).exists():
            user = Account.objects.get(электрондық_пошта__exact=email)
            current_site = get_current_site(request)
            mail_subject = 'Тіркелгіңіздің құпия сөзін қалпына келтіріңіз'
            message = render_to_string('accounts/reset_password.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.info(request, 'Құпия сөзді қалпына келтіру үшін электрондық поштаңызды тексеріңіз')
        else:
            messages.error(request, 'Аккаунт табылмады')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Жаңа құпия сөзді енгізіңіз')
        return redirect('reset_password_view')
    else:
        messages.error(request, 'Белсендіру сілтемесінің мерзімі аяқталды')
        return redirect('login')


def reset_password_view(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Құпия сөз сәтті жаңартылды')
            return redirect('login')
        else:
            messages.error(request, 'Құпия сөздер сәйкес келмейді')
            return redirect('reset_password_view')
    return render(request, 'accounts/reset_password_view.html')


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'accounts/my_orders.html', context)


@login_required(login_url='login')
def edit_profile(request):
    userprofile = UserProfile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль сәтті жаңартылды')
            return redirect('dashboard')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Құпия сөз сәтті жаңартылды')
                return redirect('change_password')
            else:
                messages.error(request, 'Ағымдағы құпия сөз дұрыс емес')
                return redirect('change_password')
        else:
            messages.error(request, 'Құпия сөздер сәйкес келмейді')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')


@login_required(login_url='login')
def order_detail(request, order_id):
    order_details = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = sum(item.product_price * item.quantity for item in order_details)
    context = {
        'order_detail': order_details,
        'order': order,
        'sub_total': subtotal
    }
    return render(request, 'accounts/order_details.html', context)
