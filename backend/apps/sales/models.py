from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum, F
from django.utils import timezone
from decimal import Decimal
from apps.products.models import Product
from apps.contacts.models import Client
from apps.users.models import User


class Order(models.Model):
    """Modelo para pedidos de venda"""
    
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Em processamento'),
        ('completed', 'Concluído'),
        ('cancelled', 'Cancelado'),
        ('delivered', 'Entregue'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('partial', 'Parcial'),
        ('paid', 'Pago'),
        ('overdue', 'Vencido'),
        ('cancelled', 'Cancelado'),
    ]
    
    # Informações básicas
    order_number = models.CharField(max_length=20, unique=True, verbose_name='Número do Pedido')
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='orders', verbose_name='Cliente')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders_created', verbose_name='Vendedor')
    
    # Status e datas
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Status')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name='Status de Pagamento')
    
    # Datas importantes
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Data de Conclusão')
    delivery_date = models.DateTimeField(null=True, blank=True, verbose_name='Data de Entrega')
    due_date = models.DateTimeField(null=True, blank=True, verbose_name='Data de Vencimento')
    
    # Valores
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Subtotal')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Desconto')
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Impostos')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Total')
    
    # Observações
    notes = models.TextField(blank=True, null=True, verbose_name='Observações')
    shipping_address = models.TextField(blank=True, null=True, verbose_name='Endereço de Entrega')
    
    class Meta:
        db_table = 'orders'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Pedido {self.order_number} - {self.client.name}"
    
    def save(self, *args, **kwargs):
        """Gera número do pedido automaticamente se não existir"""
        if not self.order_number:
            # Gera um número único sequencial
            last_order = Order.objects.all().order_by('-id').first()
            if last_order and last_order.order_number:
                last_num = int(last_order.order_number.split('-')[1])
            else:
                last_num = 0
            self.order_number = f"ORD-{last_num + 1:06d}"
        super().save(*args, **kwargs)
        # Recalcula totais após salvar
        self.calculate_totals()
    
    def calculate_totals(self):
        """Calcula os totais do pedido"""
        items = self.order_items.all()
        self.subtotal = sum(item.total for item in items)
        
        # Taxa padrão de 10% (pode ser personalizada)
        self.tax = self.subtotal * Decimal('0.10')
        
        # Total final
        self.total = self.subtotal - self.discount + self.tax
        self.save(update_fields=['subtotal', 'tax', 'total'])
    
    @property
    def item_count(self):
        """Retorna o número de itens no pedido"""
        return self.order_items.count()
    
    def mark_as_completed(self):
        """Marca o pedido como concluído e atualiza estoque"""
        if self.status != 'completed':
            self.status = 'completed'
            self.completed_at = timezone.now()
            
            # Atualiza estoque - baixa os produtos
            for item in self.order_items.all():
                if item.product:
                    item.product.quantity = max(0, item.product.quantity - item.quantity)
                    item.product.save()
            
            self.save()


class OrderItem(models.Model):
    """Modelo para itens de um pedido"""
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name='Pedido')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items', verbose_name='Produto')
    
    # Quantidade e valores
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name='Quantidade')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name='Preço Unitário')
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Desconto')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total')
    
    # Observações do item
    notes = models.TextField(blank=True, null=True, verbose_name='Observações')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    
    class Meta:
        db_table = 'order_items'
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
    
    def __str__(self):
        return f"{self.product.name} - Qtd: {self.quantity}"
    
    def save(self, *args, **kwargs):
        """Calcula o total do item antes de salvar"""
        if self.unit_price and self.quantity:
            self.total = (self.unit_price * self.quantity) - self.discount
        else:
            self.total = Decimal('0.00')
        super().save(*args, **kwargs)
    
    def get_total_with_discount(self):
        """Retorna o total com desconto aplicado"""
        total = self.unit_price * self.quantity
        return total - self.discount

