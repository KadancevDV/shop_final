from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='index'),
    path('categories/', views.categories, name='category_list'),
    path('category/<str:slug>', views.category_detail, name='category_detail'),
    path('category/<str:category>/product/<str:slug>', views.product_detail, name='product_detail'),
    path('cart', views.cart, name='cart'),
    path('cart/thanks', views.cart_thanks, name='cart'),
    path('cart_action', views.cart_action, name='cart_action'),
    path('cart_submit', views.cart_submit, name='cart_submit'),
    path('about', views.about, name='about')
] + static('media/', document_root='media')
