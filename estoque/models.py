from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
    """Categoria de produtos"""
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Supplier(models.Model):
    """Fornecedor"""
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, blank=True, null=True, unique=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Product(models.Model):
    """Produto do estoque"""
    UNIDADE_CHOICES = [
        ('UN', 'Unidade'),
        ('CX', 'Caixa'),
        ('KG', 'Quilograma'),
        ('LT', 'Litro'),
        ('MT', 'Metro'),
        ('PC', 'Peça'),
    ]

    codigo = models.CharField(max_length=50, unique=True, verbose_name='Código (SKU)', blank=True, null=True)
    nome = models.CharField(max_length=200)
    categoria = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='produtos')
    unidade = models.CharField(max_length=2, choices=UNIDADE_CHOICES, default='UN')
    quantidade_estoque = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Quantidade em Estoque'
    )
    estoque_minimo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Estoque Mínimo',
        help_text='Quantidade mínima para alerta de estoque baixo'
    )
    custo_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Custo Unitário'
    )
    ncm = models.CharField(max_length=10, blank=True, null=True, verbose_name='NCM')
    ean = models.CharField(max_length=13, blank=True, null=True, verbose_name='EAN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']

    def __str__(self):
        codigo = self.codigo if self.codigo else 'Sem SKU'
        return f"{codigo} - {self.nome}"

    def get_absolute_url(self):
        return reverse('produto_detail', kwargs={'pk': self.pk})

    @property
    def valor_total_estoque(self):
        """Calcula o valor total do estoque deste produto"""
        return self.quantidade_estoque * self.custo_unitario
    
    @property
    def estoque_baixo(self):
        """Verifica se o estoque está abaixo do mínimo"""
        if self.estoque_minimo > 0:
            return self.quantidade_estoque <= self.estoque_minimo
        return False
    
    @property
    def estoque_critico(self):
        """Verifica se o estoque está crítico (menor ou igual a 5, padrão)"""
        return self.quantidade_estoque <= 5
    
    @staticmethod
    def generate_sku():
        """Gera automaticamente um SKU no formato PROD-XXXX"""
        # Busca todos os produtos com SKU no formato PROD-XXXX
        products_with_sku = Product.objects.filter(
            codigo__startswith='PROD-'
        ).exclude(
            codigo__isnull=True
        ).exclude(
            codigo=''
        )
        
        max_number = 0
        for product in products_with_sku:
            if product.codigo:
                try:
                    # Extrai o número do SKU
                    number = int(product.codigo.split('-')[1])
                    if number > max_number:
                        max_number = number
                except (ValueError, IndexError):
                    continue
        
        # Próximo número
        next_number = max_number + 1
        
        # Formata com zeros à esquerda (4 dígitos)
        return f"PROD-{next_number:04d}"
    
    def save(self, *args, **kwargs):
        """Gera SKU automaticamente se não for fornecido"""
        # Verifica se o código está vazio ou None
        codigo_valido = self.codigo and self.codigo.strip()
        
        if not codigo_valido:
            # Gera SKU automaticamente
            self.codigo = Product.generate_sku()
            # Verifica se o SKU gerado já existe (caso raro de concorrência)
            attempts = 0
            while Product.objects.filter(codigo=self.codigo).exclude(pk=self.pk if self.pk else None).exists():
                attempts += 1
                if attempts > 100:  # Previne loop infinito
                    import time
                    self.codigo = f"PROD-{int(time.time())}"
                    break
                # Incrementa o número
                try:
                    current_num = int(self.codigo.split('-')[1])
                    self.codigo = f"PROD-{current_num + 1:04d}"
                except (ValueError, IndexError):
                    # Se algo der errado, usa timestamp como fallback
                    import time
                    self.codigo = f"PROD-{int(time.time())}"
                    break
        
        super().save(*args, **kwargs)


class StockMovement(models.Model):
    """Movimentação de estoque (entrada ou saída)"""
    MOVEMENT_TYPE_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
    ]

    tipo = models.CharField(max_length=7, choices=MOVEMENT_TYPE_CHOICES)
    produto = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movimentacoes')
    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    custo_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    fornecedor = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    observacao = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Movimentações de Estoque'
        ordering = ['-created_at']

    def __str__(self):
        tipo_label = 'Entrada' if self.tipo == 'ENTRADA' else 'Saída'
        return f"{tipo_label} - {self.produto.nome} - {self.quantidade} {self.produto.unidade}"

    def save(self, *args, **kwargs):
        """Atualiza o estoque automaticamente ao salvar a movimentação"""
        super().save(*args, **kwargs)
        
        # Atualiza quantidade em estoque
        if self.tipo == 'ENTRADA':
            self.produto.quantidade_estoque += self.quantidade
        else:  # SAIDA
            self.produto.quantidade_estoque -= self.quantidade
        
        # Atualiza custo unitário se for entrada e tiver custo informado
        if self.tipo == 'ENTRADA' and self.custo_unitario > 0:
            # Calcula média ponderada do custo
            total_atual = self.produto.quantidade_estoque - self.quantidade
            custo_atual = self.produto.custo_unitario
            if total_atual > 0:
                novo_custo = (
                    (total_atual * custo_atual) + (self.quantidade * self.custo_unitario)
                ) / self.produto.quantidade_estoque
            else:
                novo_custo = self.custo_unitario
            self.produto.custo_unitario = novo_custo
        
        self.produto.save()


class WhatsAppOrder(models.Model):
    """Pedido gerado para WhatsApp"""
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_whatsapp')
    mensagem = models.TextField(verbose_name='Mensagem do Pedido')
    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Valor Total'
    )
    total_itens = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name='Total de Itens'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pedido WhatsApp'
        verbose_name_plural = 'Pedidos WhatsApp'
        ordering = ['-created_at']

    def __str__(self):
        return f"Pedido - R$ {self.valor_total} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"
