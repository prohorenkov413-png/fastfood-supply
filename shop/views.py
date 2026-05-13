from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from .models import Category, Product, Order, OrderItem, SupportTicket
from .forms import RegistrationForm, ProfileForm, SupportForm
from decimal import Decimal
from django.http import HttpResponse

def home(request):
    products = Product.objects.all()[:6]
    return render(request, 'shop/home.html', {'products': products})

def catalog(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    products = Product.objects.all()
    if selected_category:
        products = products.filter(category__slug=selected_category)
    return render(request, 'shop/catalog.html', {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'🎉 {user.username}, вы успешно зарегистрированы!')
            return redirect('/')
        else:
            messages.error(request, 'Ошибка регистрации. Проверьте форму.')
    else:
        form = RegistrationForm()
    return render(request, 'shop/register.html', {'form': form})
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile, user=request.user)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile, user=request.user)
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/profile.html', {'form': form, 'orders': orders})

@login_required
def support(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            send_mail(
                f'Поддержка FastFood: {ticket.subject}',
                f'Здравствуйте, {request.user.username}!\n\nВаше обращение получено.\nТема: {ticket.subject}\n\nМы ответим вам в ближайшее время.\n\n---\nВаше сообщение:\n{ticket.message}',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=True,
            )
            messages.success(request, 'Ваше обращение отправлено! Ответ придёт на почту.')
            return redirect('home')
    else:
        form = SupportForm()
    tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/support.html', {'form': form, 'tickets': tickets})

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0')
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        quantity = item.get('quantity', 0)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str]['quantity'] += 1
    else:
        cart[product_id_str] = {'quantity': 1}
    request.session['cart'] = cart
    messages.success(request, 'Товар добавлен в корзину!')
    return redirect(request.META.get('HTTP_REFERER', 'catalog'))

def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 0))
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        if quantity > 0:
            cart[product_id_str]['quantity'] = quantity
        else:
            if product_id_str in cart:
                del cart[product_id_str]
        request.session['cart'] = cart
        messages.success(request, 'Корзина обновлена')
    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
    request.session['cart'] = cart
    messages.success(request, 'Товар удалён из корзины')
    return redirect('cart')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, 'Корзина пуста! Добавьте товары перед оформлением.')
        return redirect('catalog')
    
    if request.method == 'POST':
        delivery_method = request.POST.get('delivery_method')
        payment_method = request.POST.get('payment_method')
        
        order = Order.objects.create(
            user=request.user,
            delivery_method=delivery_method,
            payment_method=payment_method,
        )
        
        total = Decimal('0')
        for product_id, item in cart.items():
            product = get_object_or_404(Product, id=int(product_id))
            quantity = item['quantity']
            total += product.price * quantity
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )
        
        order.total_price = total
        order.save()
        
        request.session['cart'] = {}
        messages.success(request, f'Заказ #{order.id} успешно оформлен! Спасибо за покупку!')
        return redirect('profile')
    
    total = Decimal('0')
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        total += product.price * item['quantity']
    
    return render(request, 'shop/checkout.html', {
        'total': total,
        'delivery_methods': ['Курьером', 'Самовывоз', 'Почта России'],
        'payment_methods': ['Наличными при получении', 'Картой онлайн', 'Безналичный расчёт'],
    })

def debug_images(request):
    from shop.models import Product
    result = "<h1>Отладка картинок</h1>"
    for p in Product.objects.all():
        result += f"<p><strong>{p.name}</strong><br>"
        result += f"image поле: {p.image}<br>"
        result += f"URL: {p.image.url if p.image else 'НЕТ КАРТИНКИ'}</p>"
    return HttpResponse(result)
from django.contrib.auth import get_user_model
User = get_user_model()

# Вывести всех пользователей в консоль (логи Render)
print("=== ВСЕ ПОЛЬЗОВАТЕЛИ В БАЗЕ ===")
for u in User.objects.all():
    print(f"Логин: {u.username}, Email: {u.email}, ID: {u.id}")
print("================================")

def debug_images(request):
    from shop.models import Product
    from django.http import HttpResponse
    result = "<h1>Отладка картинок</h1>"
    for p in Product.objects.all():
        result += f"<p><strong>{p.name}</strong><br>"
        result += f"image поле: {p.image}<br>"
        result += f"URL: {p.image.url if p.image else 'НЕТ КАРТИНКИ'}</p>"
    return HttpResponse(result)