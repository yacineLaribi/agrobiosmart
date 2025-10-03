from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem
from .cart import Cart
from .forms import CheckoutForm, UserRegistrationForm


@login_required
def checkout(request):
    """Checkout page"""
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart_detail')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create order with transaction to ensure data consistency
            with transaction.atomic():
                # Create the order
                order = Order.objects.create(
                    user=request.user,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city'],
                    postal_code=form.cleaned_data['postal_code'],
                    total_price=cart.get_total_price()
                )
                
                # Create order items
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        quantity=item['quantity'],
                        price=item['price']
                    )
                    
                    # Update product stock
                    product = item['product']
                    product.stock -= item['quantity']
                    product.save()
                
                # Clear the cart
                cart.clear()
                
                messages.success(request, 'Your order has been placed successfully!')
                return redirect('checkout_success', order_id=order.id)
    else:
        # Pre-fill form with user data if available
        initial_data = {
            'email': request.user.email,
        }
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'shop/checkout.html', context)


@login_required
def checkout_success(request, order_id):
    """Order success page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order,
    }
    return render(request, 'shop/checkout_success.html', context)


def register(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'shop/register.html', context)
