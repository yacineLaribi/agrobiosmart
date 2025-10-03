from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product
from .cart import Cart


def cart_detail(request):
    """Display cart contents"""
    cart = Cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})


def cart_add(request, product_id):
    """Add product to cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        # Check stock availability
        if quantity > product.stock:
            messages.error(request, f'Only {product.stock} units available.')
            return redirect('product_detail', slug=product.slug)
        
        cart.add(product=product, quantity=quantity)
        messages.success(request, f'{product.name} added to cart.')
        
        # Redirect to cart or back to product
        if request.POST.get('redirect_to_cart'):
            return redirect('cart_detail')
        return redirect('product_detail', slug=product.slug)
    
    return redirect('product_list')


def cart_remove(request, product_id):
    """Remove product from cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'{product.name} removed from cart.')
    return redirect('cart_detail')
