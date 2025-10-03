from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import cart_views
from . import checkout_views

urlpatterns = [
    # Home and products
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Cart
    path('cart/', cart_views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', cart_views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', cart_views.cart_remove, name='cart_remove'),
    
    # Checkout
    path('checkout/', checkout_views.checkout, name='checkout'),
    path('checkout/success/<int:order_id>/', checkout_views.checkout_success, name='checkout_success'),
    
    # User account
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', checkout_views.register, name='register'),
]
