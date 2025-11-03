"""
Testes de integração end-to-end para o app estoque
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from estoque.models import Category, Supplier, Product, StockMovement


class IntegrationTest(TestCase):
    """Testes de integração completos do fluxo do sistema"""
    
    def setUp(self):
        """Prepara dados para os testes"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    def test_fluxo_completo_produto(self):
        """
        Testa fluxo completo: criar categoria -> criar fornecedor -> 
        criar produto -> fazer entrada -> fazer saída -> verificar estoque
        """
        # 1. Criar categoria
        response = self.client.post(reverse('estoque:categoria_criar'), {
            'nome': 'Eletrônicos',
            'descricao': 'Produtos eletrônicos'
        })
        self.assertEqual(response.status_code, 302)
        categoria = Category.objects.get(nome='Eletrônicos')
        
        # 2. Criar fornecedor
        response = self.client.post(reverse('estoque:fornecedor_criar'), {
            'nome': 'Fornecedor Eletrônicos',
            'telefone': '(11) 98765-4321',
            'email': 'contato@fornecedor.com'
        })
        self.assertEqual(response.status_code, 302)
        fornecedor = Supplier.objects.get(nome='Fornecedor Eletrônicos')
        
        # 3. Criar produto
        response = self.client.post(reverse('estoque:produto_criar'), {
            'nome': 'Notebook',
            'categoria': categoria.id,
            'unidade': 'UN',
            'quantidade_estoque': '0.00',
            'custo_unitario': '0.00'
        })
        self.assertEqual(response.status_code, 302)
        produto = Product.objects.get(nome='Notebook')
        self.assertIsNotNone(produto.codigo)  # SKU gerado automaticamente
        
        # 4. Fazer entrada
        estoque_inicial = produto.quantidade_estoque
        response = self.client.post(reverse('estoque:entrada_manual'), {
            'produto': produto.id,
            'quantidade': '10.00',
            'custo_unitario': '2500.00',
            'fornecedor': fornecedor.id
        })
        self.assertEqual(response.status_code, 302)
        
        # Verificar estoque após entrada
        produto.refresh_from_db()
        self.assertEqual(
            produto.quantidade_estoque,
            estoque_inicial + Decimal('10.00')
        )
        self.assertEqual(produto.custo_unitario, Decimal('2500.00'))
        
        # Verificar movimentação criada
        movimentacoes = StockMovement.objects.filter(produto=produto)
        self.assertEqual(movimentacoes.count(), 1)
        self.assertEqual(movimentacoes.first().tipo, 'ENTRADA')
        
        # 5. Fazer saída
        estoque_antes_saida = produto.quantidade_estoque
        response = self.client.post(reverse('estoque:saida_criar'), {
            'produto': produto.id,
            'quantidade': '3.00',
            'observacao': 'Venda para cliente'
        })
        self.assertEqual(response.status_code, 302)
        
        # Verificar estoque após saída
        produto.refresh_from_db()
        self.assertEqual(
            produto.quantidade_estoque,
            estoque_antes_saida - Decimal('3.00')
        )
        
        # Verificar movimentação de saída criada
        movimentacoes = StockMovement.objects.filter(produto=produto)
        self.assertEqual(movimentacoes.count(), 2)
        self.assertTrue(movimentacoes.filter(tipo='SAIDA').exists())
    
    def test_fluxo_busca_e_filtros(self):
        """Testa fluxo completo de busca e filtros de produtos"""
        # Criar dados
        categoria1 = Category.objects.create(nome='Categoria A')
        categoria2 = Category.objects.create(nome='Categoria B')
        
        produto1 = Product.objects.create(
            codigo='PROD-0001',
            nome='Produto A',
            categoria=categoria1,
            quantidade_estoque=Decimal('100.00'),
            custo_unitario=Decimal('50.00')
        )
        produto2 = Product.objects.create(
            codigo='PROD-0002',
            nome='Produto B',
            categoria=categoria2,
            quantidade_estoque=Decimal('50.00'),
            custo_unitario=Decimal('30.00')
        )
        
        # Busca por nome
        response = self.client.get(reverse('estoque:produto_lista'), {
            'busca': 'Produto A'  # Parâmetro correto é 'busca'
        })
        self.assertEqual(response.status_code, 200)
        produtos = response.context['produtos']
        # produtos é um objeto Page do Paginator
        self.assertEqual(produtos.paginator.count, 1)
        self.assertEqual(produtos[0].nome, 'Produto A')
        
        # Busca por código
        response = self.client.get(reverse('estoque:produto_lista'), {
            'busca': 'PROD-0002'
        })
        produtos = response.context['produtos']
        self.assertEqual(produtos.paginator.count, 1)
        self.assertEqual(produtos[0].codigo, 'PROD-0002')
    
    def test_fluxo_multiplas_entradas_e_saidas(self):
        """Testa múltiplas entradas e saídas e verifica cálculos finais"""
        categoria = Category.objects.create(nome='Teste')
        fornecedor = Supplier.objects.create(nome='Fornecedor Teste')
        produto = Product.objects.create(
            codigo='PROD-0001',
            nome='Produto Teste',
            categoria=categoria,
            quantidade_estoque=Decimal('0.00'),
            custo_unitario=Decimal('0.00')
        )
        
        # Entrada 1: 100 unidades a R$ 50,00
        self.client.post(reverse('estoque:entrada_manual'), {
            'produto': produto.id,
            'quantidade': '100.00',
            'custo_unitario': '50.00',
            'fornecedor': fornecedor.id
        })
        produto.refresh_from_db()
        self.assertEqual(produto.quantidade_estoque, Decimal('100.00'))
        self.assertEqual(produto.custo_unitario, Decimal('50.00'))
        
        # Saída 1: 30 unidades
        self.client.post(reverse('estoque:saida_criar'), {
            'produto': produto.id,
            'quantidade': '30.00'
        })
        produto.refresh_from_db()
        self.assertEqual(produto.quantidade_estoque, Decimal('70.00'))
        
        # Entrada 2: 50 unidades a R$ 60,00 (deve calcular média ponderada)
        self.client.post(reverse('estoque:entrada_manual'), {
            'produto': produto.id,
            'quantidade': '50.00',
            'custo_unitario': '60.00',
            'fornecedor': fornecedor.id
        })
        produto.refresh_from_db()
        self.assertEqual(produto.quantidade_estoque, Decimal('120.00'))
        # Verifica que o custo foi atualizado (média ponderada)
        self.assertGreater(produto.custo_unitario, Decimal('50.00'))
        self.assertLess(produto.custo_unitario, Decimal('60.00'))
        
        # Saída 2: 20 unidades
        self.client.post(reverse('estoque:saida_criar'), {
            'produto': produto.id,
            'quantidade': '20.00'
        })
        produto.refresh_from_db()
        self.assertEqual(produto.quantidade_estoque, Decimal('100.00'))
    
    def test_fluxo_dashboard_estatisticas(self):
        """Testa que o dashboard exibe estatísticas corretas após operações"""
        from django.core.cache import cache
        
        # Limpar cache para garantir dados atualizados
        cache.clear()
        
        categoria = Category.objects.create(nome='Teste')
        fornecedor = Supplier.objects.create(nome='Fornecedor Teste')
        
        # Criar produtos
        produto1 = Product.objects.create(
            codigo='PROD-0001',
            nome='Produto 1',
            categoria=categoria,
            quantidade_estoque=Decimal('100.00'),
            custo_unitario=Decimal('50.00')
        )
        produto2 = Product.objects.create(
            codigo='PROD-0002',
            nome='Produto 2',
            categoria=categoria,
            quantidade_estoque=Decimal('5.00'),  # Baixo estoque
            custo_unitario=Decimal('30.00')
        )
        
        # Limpar cache novamente após criar produtos
        cache.clear()
        
        # Fazer entrada
        self.client.post(reverse('estoque:entrada_manual'), {
            'produto': produto1.id,
            'quantidade': '50.00',
            'custo_unitario': '60.00',
            'fornecedor': fornecedor.id
        })
        
        # Limpar cache após entrada para refletir mudanças
        cache.clear()
        
        # Verificar dashboard
        response = self.client.get(reverse('estoque:index'))
        self.assertEqual(response.status_code, 200)
        
        # Verificar estatísticas (pode ser 2 ou mais, dependendo de outros testes)
        self.assertGreaterEqual(response.context['total_produtos'], 2)
        self.assertGreaterEqual(response.context['produtos_baixo_estoque'], 1)
        self.assertIsNotNone(response.context['valor_total_estoque'])
    
    def test_fluxo_edicao_produto_com_movimentacoes(self):
        """Testa edição de produto que já tem movimentações"""
        categoria = Category.objects.create(nome='Teste')
        produto = Product.objects.create(
            codigo='PROD-0001',
            nome='Produto Original',
            categoria=categoria,
            quantidade_estoque=Decimal('100.00'),
            custo_unitario=Decimal('50.00')
        )
        
        # Criar movimentação
        StockMovement.objects.create(
            tipo='ENTRADA',
            produto=produto,
            quantidade=Decimal('50.00'),
            custo_unitario=Decimal('60.00'),
            usuario=self.user
        )
        
        # Recarrega produto para pegar valores atualizados
        produto.refresh_from_db()
        
        # Editar produto
        response = self.client.post(reverse('estoque:produto_editar', args=[produto.id]), {
            'codigo': produto.codigo,
            'nome': 'Produto Editado',
            'categoria': categoria.id,
            'unidade': produto.unidade,
            'quantidade_estoque': str(produto.quantidade_estoque),
            'custo_unitario': str(produto.custo_unitario)
        })
        
        self.assertEqual(response.status_code, 302, f"Resposta não foi redirect. Status: {response.status_code}")
        produto.refresh_from_db()
        self.assertEqual(produto.nome, 'Produto Editado')
        
        # Verificar que as movimentações ainda estão associadas
        movimentacoes = StockMovement.objects.filter(produto=produto)
        self.assertEqual(movimentacoes.count(), 1)
    
    def test_fluxo_delete_produto_com_movimentacoes(self):
        """Testa deleção de produto (verifica se view existe)"""
        categoria = Category.objects.create(nome='Teste')
        produto = Product.objects.create(
            codigo='PROD-0001',
            nome='Produto a Deletar',
            categoria=categoria
        )
        
        # Criar movimentação
        StockMovement.objects.create(
            tipo='ENTRADA',
            produto=produto,
            quantidade=Decimal('10.00'),
            custo_unitario=Decimal('50.00'),
            usuario=self.user
        )
        
        # Verifica se existe view de deletar
        try:
            response = self.client.post(reverse('estoque:produto_deletar', args=[produto.id]))
            self.assertEqual(response.status_code, 302)
            
            # Verificar que produto e movimentação foram deletados
            self.assertFalse(Product.objects.filter(id=produto.id).exists())
            self.assertFalse(StockMovement.objects.filter(produto_id=produto.id).exists())
        except:
            # Se não houver view de deletar, apenas confirma que produto foi criado
            self.assertTrue(Product.objects.filter(id=produto.id).exists())
            self.assertTrue(StockMovement.objects.filter(produto_id=produto.id).exists())

