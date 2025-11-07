from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
import math

global_quantity = 0.0
global_amount = 0.0

def thankYou(request):
    total_quantity = request.session.get('total_quantity', 0.0)
    total_price = request.session.get('total_price', 0.0)

    
    request.session['cart'] = []  

    return render(request, 'thankyou.html', {
        'total_quantity': total_quantity,
        'total_price': total_price,
    })


def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def cartDetails(request):
    cart = request.session.get('cart', [])
    cart_empty = not bool(cart)

    cart_items = []
    total_quantity = 0
    total_price = 0.0  

    for item in cart:
        try:
            product = Product.objects.get(id=item['product_id'])
            item_quantity = item['quantity']
            item_price = float(product.price)  
            item_total_price = item_quantity * item_price

            cart_items.append({
                'id': product.id,
                'name': product.name,
                'quantity': item_quantity,
                'price_per_quantity': item_price,
                'total_price': item_total_price,
                'image_name': product.image_name,
            })

            total_quantity += item_quantity
            total_price += item_total_price
        except Product.DoesNotExist:
            continue
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity'))
        
        cart = [item for item in cart if not (item['product_id'] == product_id and quantity == 0)]
        request.session['cart'] = cart
        return JsonResponse({'cart_empty': not bool(cart)})
    request.session['total_quantity'] = total_quantity
    request.session['total_price'] = total_price

    return render(request, 'cartDetails.html', {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'cart_empty': cart_empty,
    })


@login_required
def product(request):
    products = Product.objects.all()

    
    cart = request.session.get('cart', [])
    cart_count = sum(item['quantity'] for item in cart)  
    cart_total = sum(float(item['price']) * item['quantity'] for item in cart)  
    total_cart_quantity = sum(item['quantity'] for item in cart)
    return render(request, 'Product.html', {
        'products': products,
        'total_cart_quantity': total_cart_quantity,
        'cart_count': cart_count,  
        'cart_total': cart_total, 
        
    })

def authView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))  
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def add_to_cart(request):
    if request.method == 'POST':
        product_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity', 0))

        if quantity < 1:
            return redirect('ecommerce_app:product') 

        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return redirect('product_not_found')  

        
        cart = request.session.get('cart', [])

       
        for item in cart:
            if item['product_id'] == product_id:
                
                item['quantity'] += quantity
                break
        else:
            
            cart.append({
                'product_id': product.id,  
                'quantity': quantity,
                'name': product.name,  
                'price': str(product.price),  
                'image_name': product.image_name,  
            })

        
        request.session['cart'] = cart

        
        return redirect('ecommerce_app:product')




def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity_change = int(request.POST.get('quantity'))
        
        cart = request.session.get('cart', [])
        for item in cart:
            if item['product_id'] == int(product_id):
                item['quantity'] += quantity_change
                if item['quantity'] < 1:
                    cart.remove(item)
                break
        request.session['cart'] = cart
    return redirect('ecommerce_app:cartDetails')

def logout_view(request):
    return render(request, 'logout.html')


