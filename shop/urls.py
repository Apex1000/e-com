from django.urls import path,include
from .views import *
app_name = 'shop'
urlpatterns = [
    path('',index, name='shop_index'),
    path('product/<slug>/',productDetails, name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('order-summary/', ordersummary, name='order-summary'),
    path('checkout/', checkout, name='checkout'),
    path('payment/<payment_option>/', payment, name='payment'),
    path('admin-cart/', admin, name='admin'),
]
