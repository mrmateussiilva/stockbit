from django.db import models
from django.core.validators import RegexValidator


class Client(models.Model):
    """Modelo para clientes"""
    
    TYPE_CHOICES = [
        ('individual', 'Pessoa Física'),
        ('company', 'Pessoa Jurídica'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Nome/Razão Social')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='individual', verbose_name='Tipo')
    
    # Dados pessoais/empresariais
    cpf_cnpj = models.CharField(
        max_length=18, 
        unique=True,
        verbose_name='CPF/CNPJ',
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$',
                message='Formato inválido. Use: 000.000.000-00 ou 00.000.000/0000-00'
            )
        ]
    )
    
    # Contato
    email = models.EmailField(blank=True, null=True, verbose_name='E-mail')
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name='Telefone',
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
                message='Formato inválido. Use: (00) 0000-0000'
            )
        ]
    )
    cellphone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name='Celular',
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
                message='Formato inválido. Use: (00) 0000-0000'
            )
        ]
    )
    
    # Endereço
    address = models.CharField(max_length=300, blank=True, null=True, verbose_name='Endereço')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Cidade')
    state = models.CharField(max_length=2, blank=True, null=True, verbose_name='Estado')
    zip_code = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        verbose_name='CEP',
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{3}$',
                message='Formato inválido. Use: 00000-000'
            )
        ]
    )
    
    # Status e observações
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    notes = models.TextField(blank=True, null=True, verbose_name='Observações')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.cpf_cnpj})"
    
    @property
    def full_address(self):
        """Retorna o endereço completo formatado"""
        parts = [self.address, self.city, self.state, self.zip_code]
        return ', '.join(filter(None, parts))


class Supplier(models.Model):
    """Modelo para fornecedores"""
    
    TYPE_CHOICES = [
        ('individual', 'Pessoa Física'),
        ('company', 'Pessoa Jurídica'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Nome/Razão Social')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='company', verbose_name='Tipo')
    
    # Dados empresariais
    cpf_cnpj = models.CharField(
        max_length=18, 
        unique=True,
        verbose_name='CPF/CNPJ',
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{2}\.\d{3}\.\d{3}\/\d{4}-\d{2}$',
                message='Formato inválido. Use: 000.000.000-00 ou 00.000.000/0000-00'
            )
        ]
    )
    
    # Contato comercial
    email = models.EmailField(blank=True, null=True, verbose_name='E-mail')
    phone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name='Telefone',
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
                message='Formato inválido. Use: (00) 0000-0000'
            )
        ]
    )
    cellphone = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        verbose_name='Celular',
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
                message='Formato inválido. Use: (00) 0000-0000'
            )
        ]
    )
    
    # Endereço
    address = models.CharField(max_length=300, blank=True, null=True, verbose_name='Endereço')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Cidade')
    state = models.CharField(max_length=2, blank=True, null=True, verbose_name='Estado')
    zip_code = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        verbose_name='CEP',
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{3}$',
                message='Formato inválido. Use: 00000-000'
            )
        ]
    )
    
    # Informações comerciais
    contact_person = models.CharField(max_length=100, blank=True, null=True, verbose_name='Pessoa de Contato')
    payment_terms = models.CharField(max_length=100, blank=True, null=True, verbose_name='Condições de Pagamento')
    delivery_time = models.CharField(max_length=50, blank=True, null=True, verbose_name='Prazo de Entrega')
    
    # Status e observações
    is_active = models.BooleanField(default=True, verbose_name='Ativo')
    notes = models.TextField(blank=True, null=True, verbose_name='Observações')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')
    
    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.cpf_cnpj})"
    
    @property
    def full_address(self):
        """Retorna o endereço completo formatado"""
        parts = [self.address, self.city, self.state, self.zip_code]
        return ', '.join(filter(None, parts))