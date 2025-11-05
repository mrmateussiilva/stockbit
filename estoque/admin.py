from django.contrib import admin
from .models import Product, Category, Supplier, StockMovement, WhatsAppOrder


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'created_at']
    search_fields = ['nome', 'descricao']
    ordering = ['nome']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'telefone', 'email']
    search_fields = ['nome', 'cnpj']
    ordering = ['nome']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nome', 'categoria', 'unidade', 'quantidade_estoque', 'custo_unitario']
    list_filter = ['categoria', 'unidade']
    search_fields = ['codigo', 'nome', 'ncm', 'ean']
    ordering = ['nome']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'produto', 'quantidade', 'custo_unitario', 'created_at', 'usuario']
    list_filter = ['tipo', 'created_at', 'fornecedor']
    search_fields = ['produto__nome', 'produto__codigo', 'observacao']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(WhatsAppOrder)
class WhatsAppOrderAdmin(admin.ModelAdmin):
    list_display = ['valor_total', 'total_itens', 'usuario', 'created_at']
    list_filter = ['created_at', 'usuario']
    search_fields = ['mensagem', 'usuario__username']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'mensagem']
    date_hierarchy = 'created_at'
