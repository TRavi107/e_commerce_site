from django.urls import path,include
from .views import (
    HomeView,
    ItemDetailView,
    add_to_cart,
    remove_from_cart,
    CheckOutView,
    remove_from_cart_c,
    add_to_cart_c,
    remove_from_cart_all,
    PaymentView,
    like_the_comment,
    filter_by_categories
)

app_name= 'core'

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('categories=<categories>/',filter_by_categories,name='filter_by_categories'),
    path('product/<slug>/',ItemDetailView.as_view(),name='product'),
    path('add_to_cart/<slug>/',add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<slug>/',remove_from_cart,name='remove_from_cart'),
    path('CheckOutVIew/',CheckOutView.as_view(),name='CheckOutView'),
    path('remove_from_cart_c/<slug>/',remove_from_cart_c,name='remove_from_cart_c'),
    path('like_the_comment/<id>/',like_the_comment,name='like_the_comment'),
    path('add_to_cart_c/<slug>/',add_to_cart_c,name='add_to_cart_c'),
    path('remove_from_cart_all/<slug>/',remove_from_cart_all,name='remove_from_cart_all'),
    path('payment/<payment_option>',PaymentView.as_view(),name='payment')

]