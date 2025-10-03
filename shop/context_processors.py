from .cart import Cart


def cart_count(request):
    """Add cart item count to all templates"""
    cart = Cart(request)
    return {'cart_count': len(cart)}
