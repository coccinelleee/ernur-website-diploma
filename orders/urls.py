from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('submit_review/<int:order_product_id>/', views.submit_review, name='submit_review'),
]