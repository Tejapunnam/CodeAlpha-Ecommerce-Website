
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, CartItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# ---------------- HOME ----------------

def home(request):
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0

    return render(request, "home.html", {
        "cart_count": cart_count
    })

# ---------------- PRODUCTS ----------------

@login_required
def products(request):
    query = request.GET.get("q", "")

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    if request.user.is_authenticated:
       cart_count = CartItem.objects.filter(user=request.user).count()
    else:
       cart_count = 0

    return render(request, "products.html", {
        "products": products,
        "query": query,
        "cart_count": cart_count
    })

# ---------------- PRODUCT DETAIL ----------------

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
       cart_count = CartItem.objects.filter(user=request.user).count()
    else:
       cart_count = 0
    return render(request, "product_detail.html", {
        "product": product,
        "cart_count": cart_count
    })


# ---------------- ADD TO CART ----------------

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
    user=request.user,
    product=product
    )
    

    if created:
        messages.success(
            request,
            f"✅ {product.name} added to cart successfully!"
        )
    else:
        cart_item.quantity += 1
        cart_item.save()

        messages.success(
            request,
            f"✅ {product.name} quantity updated in cart!"
        )

    return redirect("products")

# ---------------- CART ----------------

@login_required
def cart(request):

    cart_items = CartItem.objects.filter(user=request.user)
    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    cart_count = CartItem.objects.filter(user=request.user).count()

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total,
        "cart_count": cart_count
    })


# ---------------- REMOVE ITEM ----------------

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(
    CartItem,
    id=item_id,
    user=request.user
)
    item.delete()

    return redirect("cart")


# ---------------- INCREASE QUANTITY ----------------

@login_required
def increase_quantity(request, item_id):

    item = get_object_or_404(
    CartItem,
    id=item_id,
    user=request.user
)

    item.quantity += 1
    item.save()

    return redirect("cart")


# ---------------- DECREASE QUANTITY ----------------

@login_required
def decrease_quantity(request, item_id):

    item = get_object_or_404(
    CartItem,
    id=item_id,
    user=request.user
)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart")


# ---------------- CHECKOUT ----------------

@login_required
def checkout(request):
    CartItem.objects.filter(
        user=request.user
    ).delete()

    return render(request, "success.html")

# ---------------- REGISTER ----------------

from django.contrib import messages

def register(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("register")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Registration Successful! Please Login.")
        return redirect("login")

    return render(request, "register.html")
# ---------------- LOGIN ----------------

def user_login(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.username}! 👋"
            )

            return redirect("home")

        else:

            messages.error(
                request,
                "Invalid Username or Password."
            )

            return redirect("login")

    return render(request, "login.html")

# ---------------- LOGOUT ----------------

def user_logout(request):

    logout(request)

    return redirect("home")