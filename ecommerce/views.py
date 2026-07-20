from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, CartItem
from store.models import CartItem
from django.shortcuts import get_object_or_404

def checkout(request):

    cart_items = CartItem.objects.all()

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    if request.method == "POST":
        cart_items.delete()
        return render(request, "success.html")

    return render(request, "checkout.html", {"total": total})

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')

def cart(request):
    cart_items = CartItem.objects.all()

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total
    })

def home(request):
    return render(request, "home.html")


def products(request):
    products = Product.objects.all()

    return render(request, "products.html", {
        "products": products
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('products')