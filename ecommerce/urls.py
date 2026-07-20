from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),

    path('products/', views.products, name='products'),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('cart/', views.cart, name='cart'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('checkout/', views.checkout, name='checkout'),

    path('increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),

    path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
]