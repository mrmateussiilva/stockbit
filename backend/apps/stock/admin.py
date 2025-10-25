from django.contrib import admin
from .models import StockMovement


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'reason', 'user', 'created_at']
    list_filter = ['movement_type', 'created_at', 'user']
    search_fields = ['product__name', 'product__sku', 'reason', 'notes']
    ordering = ['-created_at']
    readonly_fields = ['created_at']


