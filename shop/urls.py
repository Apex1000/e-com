from django.urls import path,include
from .views import *
app_name = 'shop'
urlpatterns = [
    path('',index, name='shop_index'),
    path('product/<slug>/',productDetails, name='product'),
]
