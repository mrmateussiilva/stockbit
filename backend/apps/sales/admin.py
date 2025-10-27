from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Admin inline para itens do pedido"""
    model = OrderItem
    extra = 1
    fields = ['product', 'quantity', 'unit_price', 'discount', 'total', 'notes']
    readonly_fields = ['total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin para pedidos"""
    list_display = [
        'order_number', 'client', 'status', 'payment_status', 
        'total', 'created_at', 'item_count'
    ]
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'client__name', 'notes']
    readonly_fields = ['order_number', 'subtotal', 'tax', 'total', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('order_number', 'client', 'user', 'status', 'payment_status')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at', 'completed_at', 'delivery_date', 'due_date')
        }),
        ('Valores', {
            'fields': ('subtotal', 'discount', 'tax', 'total')
        }),
        ('Observações', {
            'fields': ('notes', 'shipping_address'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin para itens do pedido"""
    list_display = ['order', 'product', 'quantity', 'unit_price', 'total']
    list_filter = ['created_at', 'order__status']
    search_fields = ['product__name', 'order__order_number']
    readonly_fields = ['total']


