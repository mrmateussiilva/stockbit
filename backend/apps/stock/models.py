from django.db import models
from django.core.validators import MinValueValidator
from apps.products.models import Product
from apps.users.models import User


class StockMovement(models.Model):
    """Modelo para movimentações de estoque"""
    
    MOVEMENT_TYPES = [
        ('in', 'Entrada'),
        ('out', 'Saída'),
        ('adjustment', 'Ajuste'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    reason = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stock_movements')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stock_movements'
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Movimentações de Estoque'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} - {self.get_movement_type_display()} ({self.quantity})"

    def save(self, *args, **kwargs):
        """Salva a movimentação e atualiza o estoque do produto"""
        super().save(*args, **kwargs)
        self.update_product_stock()

    def update_product_stock(self):
        """Atualiza a quantidade em estoque do produto"""
        if self.movement_type == 'in':
            self.product.quantity += self.quantity
        elif self.movement_type == 'out':
            self.product.quantity = max(0, self.product.quantity - self.quantity)
        elif self.movement_type == 'adjustment':
            self.product.quantity = self.quantity
        
        self.product.save(update_fields=['quantity'])


