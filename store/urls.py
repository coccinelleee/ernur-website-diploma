from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from stores import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('store/', include('stores.urls')),  
    path('cart/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('currencies/', include('currencies.urls')),
    path('selectcurrency', views.selectcurrency, name='selectcurrency'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_details, name='product_details'),
    path('savelangcur', views.savelangcur, name='savelangcur'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
