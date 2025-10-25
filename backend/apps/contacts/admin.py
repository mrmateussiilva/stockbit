from django.contrib import admin
from .models import Client, Supplier


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'cpf_cnpj', 'email', 'phone', 'city', 'is_active', 'created_at']
    list_filter = ['type', 'is_active', 'state', 'created_at']
    search_fields = ['name', 'cpf_cnpj', 'email', 'phone']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'type', 'cpf_cnpj', 'is_active')
        }),
        ('Contato', {
            'fields': ('email', 'phone', 'cellphone')
        }),
        ('Endereço', {
            'fields': ('address', 'city', 'state', 'zip_code')
        }),
        ('Observações', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'cpf_cnpj', 'email', 'contact_person', 'city', 'is_active', 'created_at']
    list_filter = ['type', 'is_active', 'state', 'created_at']
    search_fields = ['name', 'cpf_cnpj', 'email', 'phone', 'contact_person']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'type', 'cpf_cnpj', 'is_active')
        }),
        ('Contato', {
            'fields': ('email', 'phone', 'cellphone', 'contact_person')
        }),
        ('Endereço', {
            'fields': ('address', 'city', 'state', 'zip_code')
        }),
        ('Informações Comerciais', {
            'fields': ('payment_terms', 'delivery_time')
        }),
        ('Observações', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )