import os
import django
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.products.models import Category, Product
from apps.stock.models import StockMovement
from apps.contacts.models import Client, Supplier
from decimal import Decimal

User = get_user_model()

def create_initial_data():
    """Cria dados iniciais para o sistema"""
    
    # Criar usuário admin
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@stockbit.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema',
            is_staff=True,
            is_superuser=True
        )
        print(f"Usuário admin criado: {admin_user.email}")
    else:
        admin_user = User.objects.get(username='admin')
        print("Usuário admin já existe")

    # Criar categorias para empresa de tecidos, papéis e tintas
    categories_data = [
        {'name': 'Tecidos', 'description': 'Tecidos diversos para confecção e decoração'},
        {'name': 'Papéis', 'description': 'Papéis para impressão, embalagem e decoração'},
        {'name': 'Tintas', 'description': 'Tintas para tecidos, papéis e superfícies diversas'},
        {'name': 'Acessórios', 'description': 'Linhas, botões, zíperes e outros acessórios'},
        {'name': 'Ferramentas', 'description': 'Ferramentas para corte, costura e acabamento'},
    ]

    created_categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        created_categories.append(category)
        if created:
            print(f"Categoria criada: {category.name}")

    # Criar produtos de exemplo para empresa de tecidos, papéis e tintas
    products_data = [
        {
            'name': 'Tecido Algodão 100% - Branco',
            'description': 'Tecido de algodão 100% branco, ideal para confecção de camisetas',
            'sku': 'TEC-ALG-BRANCO-001',
            'category': created_categories[0],
            'price': Decimal('25.90'),
            'quantity': 50,
            'min_quantity': 10,
        },
        {
            'name': 'Tecido Jeans Azul - 1 metro',
            'description': 'Tecido jeans azul escuro, perfeito para calças e jaquetas',
            'sku': 'TEC-JEANS-AZUL-001',
            'category': created_categories[0],
            'price': Decimal('35.90'),
            'quantity': 30,
            'min_quantity': 8,
        },
        {
            'name': 'Papel A4 75g - Pacote 500 folhas',
            'description': 'Papel A4 branco 75g, ideal para impressão e escritório',
            'sku': 'PAP-A4-75G-001',
            'category': created_categories[1],
            'price': Decimal('18.90'),
            'quantity': 100,
            'min_quantity': 20,
        },
        {
            'name': 'Papel Kraft Marrom - 1 metro',
            'description': 'Papel kraft marrom para embalagem e decoração',
            'sku': 'PAP-KRAFT-MARROM-001',
            'category': created_categories[1],
            'price': Decimal('12.50'),
            'quantity': 80,
            'min_quantity': 15,
        },
        {
            'name': 'Tinta para Tecido - Azul',
            'description': 'Tinta especial para tecidos, cor azul, resistente à lavagem',
            'sku': 'TIN-TECIDO-AZUL-001',
            'category': created_categories[2],
            'price': Decimal('8.90'),
            'quantity': 25,
            'min_quantity': 5,
        },
        {
            'name': 'Tinta Acrílica Branca - 500ml',
            'description': 'Tinta acrílica branca para papel e superfícies diversas',
            'sku': 'TIN-ACRILICA-BRANCA-001',
            'category': created_categories[2],
            'price': Decimal('15.90'),
            'quantity': 40,
            'min_quantity': 8,
        },
        {
            'name': 'Linha de Costura Branca - 100m',
            'description': 'Linha de costura branca 100% poliéster, resistente',
            'sku': 'LIN-COSTURA-BRANCA-001',
            'category': created_categories[3],
            'price': Decimal('3.50'),
            'quantity': 200,
            'min_quantity': 50,
        },
        {
            'name': 'Botões de Plástico Brancos - Pacote 50',
            'description': 'Botões de plástico brancos, tamanho médio',
            'sku': 'BOT-PLASTICO-BRANCO-001',
            'category': created_categories[3],
            'price': Decimal('12.90'),
            'quantity': 15,
            'min_quantity': 5,
        },
        {
            'name': 'Tesoura para Tecido - 20cm',
            'description': 'Tesoura profissional para corte de tecidos',
            'sku': 'TES-TECIDO-20CM-001',
            'category': created_categories[4],
            'price': Decimal('45.90'),
            'quantity': 8,
            'min_quantity': 2,
        },
        {
            'name': 'Régua de Corte - 60cm',
            'description': 'Régua de corte transparente com marcações precisas',
            'sku': 'REG-CORTE-60CM-001',
            'category': created_categories[4],
            'price': Decimal('28.90'),
            'quantity': 12,
            'min_quantity': 3,
        },
    ]

    created_products = []
    for prod_data in products_data:
        product, created = Product.objects.get_or_create(
            sku=prod_data['sku'],
            defaults=prod_data
        )
        created_products.append(product)
        if created:
            print(f"Produto criado: {product.name}")

    # Criar algumas movimentações de exemplo
    movements_data = [
        {
            'product': created_products[0],
            'movement_type': 'in',
            'quantity': 20,
            'reason': 'Compra de estoque inicial',
            'notes': 'Entrada inicial de tecido algodão',
            'user': admin_user,
        },
        {
            'product': created_products[2],
            'movement_type': 'in',
            'quantity': 50,
            'reason': 'Reposição de estoque',
            'notes': 'Reposição de papel A4',
            'user': admin_user,
        },
        {
            'product': created_products[4],
            'movement_type': 'out',
            'quantity': 5,
            'reason': 'Venda',
            'notes': 'Venda de tinta para tecido',
            'user': admin_user,
        },
        {
            'product': created_products[6],
            'movement_type': 'adjustment',
            'quantity': 180,
            'reason': 'Ajuste de inventário',
            'notes': 'Ajuste após contagem física',
            'user': admin_user,
        },
    ]

    for mov_data in movements_data:
        movement, created = StockMovement.objects.get_or_create(
            product=mov_data['product'],
            movement_type=mov_data['movement_type'],
            quantity=mov_data['quantity'],
            reason=mov_data['reason'],
            defaults={
                'notes': mov_data['notes'],
                'user': mov_data['user'],
            }
        )
        if created:
            print(f"Movimentação criada: {movement}")

    print("\n✅ Dados iniciais criados com sucesso!")
    print(f"📊 Total de categorias: {Category.objects.count()}")
    print(f"📦 Total de produtos: {Product.objects.count()}")
    print(f"📈 Total de movimentações: {StockMovement.objects.count()}")
    print(f"👤 Usuário admin: admin / admin123")
    
    # Criar dados de exemplo para clientes
    clients_data = [
        {
            'name': 'Maria Silva',
            'type': 'individual',
            'cpf_cnpj': '111.444.777-35',
            'email': 'maria.silva@email.com',
            'phone': '(11) 9999-1111',
            'cellphone': '(11) 9999-1111',
            'address': 'Rua das Flores, 123',
            'city': 'São Paulo',
            'state': 'SP',
            'zip_code': '01234-567',
            'notes': 'Cliente preferencial',
        },
        {
            'name': 'João Santos',
            'type': 'individual',
            'cpf_cnpj': '222.555.888-46',
            'email': 'joao.santos@email.com',
            'phone': '(11) 8888-2222',
            'cellphone': '(11) 8888-2222',
            'address': 'Av. Paulista, 456',
            'city': 'São Paulo',
            'state': 'SP',
            'zip_code': '01310-100',
            'notes': 'Cliente frequente',
        },
        {
            'name': 'Confeccões ABC Ltda',
            'type': 'company',
            'cpf_cnpj': '12.345.678/0001-90',
            'email': 'contato@confeccoesabc.com',
            'phone': '(11) 3333-3333',
            'cellphone': '(11) 9999-3333',
            'address': 'Rua Industrial, 789',
            'city': 'São Paulo',
            'state': 'SP',
            'zip_code': '03123-456',
            'notes': 'Empresa de confecção',
        },
        {
            'name': 'Ana Costa',
            'type': 'individual',
            'cpf_cnpj': '333.666.999-57',
            'email': 'ana.costa@email.com',
            'phone': '(11) 7777-3333',
            'cellphone': '(11) 7777-3333',
            'address': 'Rua da Paz, 321',
            'city': 'São Paulo',
            'state': 'SP',
            'zip_code': '04567-890',
            'notes': 'Cliente novo',
        },
    ]

    for client_data in clients_data:
        client, created = Client.objects.get_or_create(
            cpf_cnpj=client_data['cpf_cnpj'],
            defaults=client_data
        )
        if created:
            print(f"Cliente criado: {client}")

    # Criar dados de exemplo para fornecedores
    suppliers_data = [
        {
            'name': 'Tecidos ABC Ltda',
            'type': 'company',
            'cpf_cnpj': '11.222.333/0001-81',
            'email': 'contato@tecidosabc.com',
            'phone': '(11) 3333-4444',
            'cellphone': '(11) 9999-4444',
            'address': 'Rua dos Tecidos, 100',
            'city': 'São Paulo',
            'state': 'SP',
            'zip_code': '01234-567',
            'contact_person': 'Maria Santos',
            'payment_terms': '30 dias',
            'delivery_time': '7 dias úteis',
            'notes': 'Fornecedor principal de tecidos',
        },
        {
            'name': 'Papéis & Cia Ltda',
            'type': 'company',
            'cpf_cnpj': '22.333.444/0001-92',
            'email': 'vendas@papeisecia.com',
            'phone': '(11) 4444-5555',
            'cellphone': '(11) 9999-5555',
            'address': 'Av. dos Papéis, 200',
            'city': 'São Paulo',
            'state': 'SP',
            'zip_code': '02345-678',
            'contact_person': 'Carlos Oliveira',
            'payment_terms': '15 dias',
            'delivery_time': '5 dias úteis',
            'notes': 'Especialista em papéis especiais',
        },
        {
            'name': 'Tintas Coloridas Ltda',
            'type': 'company',
            'cpf_cnpj': '33.444.555/0001-03',
            'email': 'comercial@tintascoloridas.com',
            'phone': '(11) 5555-6666',
            'cellphone': '(11) 9999-6666',
            'address': 'Rua das Tintas, 300',
            'city': 'São Paulo',
            'state': 'SP',
            'zip_code': '03456-789',
            'contact_person': 'Pedro Lima',
            'payment_terms': '45 dias',
            'delivery_time': '10 dias úteis',
            'notes': 'Fornecedor de tintas profissionais',
        },
        {
            'name': 'Acessórios Rápidos',
            'type': 'company',
            'cpf_cnpj': '44.555.666/0001-14',
            'email': 'pedidos@acessoriosrapidos.com',
            'phone': '(11) 6666-7777',
            'cellphone': '(11) 9999-7777',
            'address': 'Rua dos Acessórios, 400',
            'city': 'São Paulo',
            'state': 'SP',
            'zip_code': '04567-890',
            'contact_person': 'Fernanda Costa',
            'payment_terms': '20 dias',
            'delivery_time': '3 dias úteis',
            'notes': 'Entrega rápida de acessórios',
        },
    ]

    for supplier_data in suppliers_data:
        supplier, created = Supplier.objects.get_or_create(
            cpf_cnpj=supplier_data['cpf_cnpj'],
            defaults=supplier_data
        )
        if created:
            print(f"Fornecedor criado: {supplier}")

    print(f"👥 Total de clientes: {Client.objects.count()}")
    print(f"🚚 Total de fornecedores: {Supplier.objects.count()}")

if __name__ == '__main__':
    create_initial_data()

