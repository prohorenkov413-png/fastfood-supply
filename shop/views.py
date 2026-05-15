from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from .models import Category, Product, Order, OrderItem, SupportTicket
from .forms import RegistrationForm, ProfileForm, SupportForm
from decimal import Decimal

from django.contrib.auth import get_user_model
from shop.models import Category, Product

User = get_user_model()

# Создаём админа, если нет
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✅ Админ создан: admin / admin123")

# Создаём категории и товары
categories_data = [
    {'name': 'Упаковка', 'slug': 'upakovka'},
    {'name': 'Расходные материалы', 'slug': 'rashodniki'},
    {'name': 'Одноразовая посуда', 'slug': 'posuda'},
]

products_data = [
    # Упаковка
    ('upakovka', 'Бургер-бокс', 'burger-box', 'Картонный, для гамбургеров. 50 шт', 1500, 100, '🍔'),
    ('upakovka', 'Ланч-бокс', 'lanch-box', 'Для сэндвичей. 50 шт', 1200, 80, '📦'),
    ('upakovka', 'Бумажные кульки', 'kulki', 'Для картошки фри. 100 шт', 600, 200, '🍟'),
    ('upakovka', 'Пицца-бокс', 'pizza-box', 'Диаметр 30 см. 25 шт', 1800, 40, '🍕'),
    ('upakovka', 'Ведёрко для попкорна', 'popcorn', 'Картонное. 50 шт', 700, 90, '🍿'),
    ('upakovka', 'Пакет бумажный', 'paket', 'С откидным дном. 100 шт', 850, 150, '🛍️'),
    ('upakovka', 'Контейнер для крыльев', 'krylya', 'Три отделения. 50 шт', 900, 60, '🍗'),
    ('upakovka', 'Коробка для наггетсов', 'naggets', 'Маленькая. 100 шт', 500, 120, '🐔'),
    ('upakovka', 'Салатник пластиковый', 'salatnik', '500 мл. 30 шт', 450, 100, '🥗'),
    ('upakovka', 'Лоток для упаковки', 'lotok', 'Прямоугольный. 50 шт', 350, 150, '📦'),
    # Расходные материалы
    ('rashodniki', 'Перчатки нитриловые', 'perchatki-nitril', '100 шт, размер M', 2500, 100, '🧤'),
    ('rashodniki', 'Перчатки виниловые', 'perchatki-vinil', '100 шт, универсальные', 1500, 100, '🧤'),
    ('rashodniki', 'Перчатки латексные', 'perchatki-latex', '100 шт, размер L', 2000, 80, '🧤'),
    ('rashodniki', 'Бумажные салфетки', 'salfetki', '33x33 см, 500 шт', 800, 200, '🧻'),
    ('rashodniki', 'Влажные салфетки', 'salfetki-vlazhnye', 'Индивидуальные, 100 шт', 600, 150, '💧'),
    ('rashodniki', 'Трубочки пластиковые', 'trubochki', 'Диаметр 6 мм, 100 шт', 300, 500, '🥤'),
    ('rashodniki', 'Ложки одноразовые', 'lozhki', 'Пластиковые, 100 шт', 400, 300, '🥄'),
    ('rashodniki', 'Вилки одноразовые', 'vilki', 'Пластиковые, 100 шт', 400, 300, '🍴'),
    ('rashodniki', 'Ножи одноразовые', 'nozhi', 'Пластиковые, 100 шт', 350, 250, '🔪'),
    ('rashodniki', 'Фартуки одноразовые', 'fartuki', 'Полиэтиленовые, 100 шт', 1200, 50, '🧥'),
    # Одноразовая посуда
    ('posuda', 'Тарелки бумажные 15см', 'tarelki-bum-15', '50 шт, экологичные', 450, 200, '🍽️'),
    ('posuda', 'Тарелки бумажные 20см', 'tarelki-bum-20', '50 шт, для горячих блюд', 550, 150, '🍽️'),
    ('posuda', 'Тарелки пластиковые', 'tarelki-plast', '50 шт, белые', 350, 300, '🥏'),
    ('posuda', 'Набор вилка+ложка+нож', 'nabor-pribory', 'Пластик, 50 наборов', 600, 200, '🍴'),
    ('posuda', 'Стаканы 0.2л эспрессо', 'stakan-02', '100 шт, для кофе', 400, 180, '☕'),
    ('posuda', 'Стаканы 0.3л', 'stakan-03', '50 шт, для напитков', 350, 200, '🥤'),
    ('posuda', 'Стаканы 0.5л', 'stakan-05', '50 шт, с крышкой', 550, 150, '🥤'),
    ('posuda', 'Крышки для стаканов', 'krishki', '100 шт, плоские', 250, 300, '🔘'),
    ('posuda', 'Контейнеры для соусов', 'sous', '30 мл с крышкой, 50 шт', 300, 400, '🥫'),
    ('posuda', 'Деревянные палочки', 'palochki', '100 пар, для суши', 200, 500, '🥢'),
]

# Создаём категории
for cat in categories_data:
    Category.objects.get_or_create(name=cat['name'], slug=cat['slug'])

# Создаём товары
for slug_cat, name, slug_prod, desc, price, stock, emoji in products_data:
    try:
        cat = Category.objects.get(slug=slug_cat)
        Product.objects.get_or_create(
            slug=slug_prod,
            defaults={
                'category': cat,
                'name': name,
                'description': desc,
                'price': price,
                'stock': stock,
                'emoji': emoji,
            }
        )
    except Exception as e:
        print(f'Ошибка с {name}: {e}')

print("✅ База данных заполнена!")

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
                f'Ваше обращение получено!\n\n{ticket.message}',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=True,
            )
            messages.success(request, 'Ваше обращение отправлено!')
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
        messages.warning(request, 'Корзина пуста!')
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
        messages.success(request, f'Заказ #{order.id} оформлен!')
        return redirect('profile')
    
    total = Decimal('0')
    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        total += product.price * item['quantity']
    
    return render(request, 'shop/checkout.html', {
        'total': total,
        'delivery_methods': ['Курьером', 'Самовывоз', 'Почта России'],
        'payment_methods': ['Наличными', 'Картой онлайн', 'Безналичный расчёт'],
    })