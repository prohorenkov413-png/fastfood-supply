# -*- coding: utf-8 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fastfood_project.settings')
import django
django.setup()

from shop.models import Product

# Словарь: название товара -> имя файла картинки
images = {
    'Бургер-бокс': 'burger-box.jpg',
    'Перчатки нитриловые': 'perchatki.jpg',
    'Стаканы 0.3л': 'stakany.jpg',
    'Салфетки бумажные': 'salfetki.jpg',
    'Ланч-бокс': 'lanch-box.jpg',
}

for product_name, image_file in images.items():
    try:
        product = Product.objects.get(name=product_name)
        product.image = f'products/{image_file}'
        product.save()
        print(f'✓ Картинка добавлена: {product_name}')
    except Product.DoesNotExist:
        print(f'✗ Товар не найден: {product_name}')
    except Exception as e:
        print(f'✗ Ошибка с {product_name}: {e}')

print('\nГотово! Все картинки добавлены.')