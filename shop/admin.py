from django.contrib import admin
from .models import Category, Product, Order, OrderItem, SupportTicket, CustomerProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('emoji', 'name', 'price', 'stock'))  # какие поля показывать
    list_filter = ('category', 'stock')  # фильтры справа
    search_fields = ('name', 'description')  # поиск
    list_editable = ('price', 'stock')  # можно редактировать прямо в списке
    list_display = ('emoji', 'name', 'price', 'stock', 'category')
    fields = ('category', 'name', 'slug', 'description', 'price', 'stock', 'image', 'emoji')  

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total_price')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'created_at', 'is_resolved')
    list_filter = ('is_resolved',)

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')