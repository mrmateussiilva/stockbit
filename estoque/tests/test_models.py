"""
Testes unitários para os modelos do app estoque
"""
from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from estoque.models import Category, Supplier, Product, StockMovement


class CategoryModelTest(TestCase):
    """Testes para o modelo Category"""
    
    def setUp(self):
        """Prepara dados para os testes"""
        self.categoria = Category.objects.create(
            nome='Eletrônicos',
            descricao='Produtos eletrônicos em geral'
        )
    
    def test_categoria_criacao(self):
        """Testa a criação de uma categoria"""
        self.assertEqual(self.categoria.nome, 'Eletrônicos')
        self.assertEqual(self.categoria.descricao, 'Produtos eletrônicos em geral')
        self.assertIsNotNone(self.categoria.created_at)
        self.assertIsNotNone(self.categoria.updated_at)
    
    def test_categoria_str(self):
        """Testa a representação em string"""
        self.assertEqual(str(self.categoria), 'Eletrônicos')
    
    def test_categoria_unique_nome(self):
        """Testa que o nome da categoria deve ser único"""
        with self.assertRaises(Exception):
            Category.objects.create(nome='Eletrônicos')


class SupplierModelTest(TestCase):
    """Testes para o modelo Supplier"""
    
    def setUp(self):
        """Prepara dados para os testes"""
        self.fornecedor = Supplier.objects.create(
            nome='Fornecedor Teste',
            cnpj='12.345.678/0001-90',
            telefone='(11) 98765-4321',
            email='contato@fornecedor.com',
            endereco='Rua Teste, 123'
        )
    
    def test_fornecedor_criacao(self):
        """Testa a criação de um fornecedor"""
        self.assertEqual(self.fornecedor.nome, 'Fornecedor Teste')
        self.assertEqual(self.fornecedor.cnpj, '12.345.678/0001-90')
        self.assertEqual(self.fornecedor.telefone, '(11) 98765-4321')
        self.assertEqual(self.fornecedor.email, 'contato@fornecedor.com')
    
    def test_fornecedor_str(self):
        """Testa a representação em string"""
        self.assertEqual(str(self.fornecedor), 'Fornecedor Teste')
    
    def test_fornecedor_unique_cnpj(self):
        """Testa que o CNPJ deve ser único"""
        with self.assertRaises(Exception):
            Supplier.objects.create(
                nome='Outro Fornecedor',
                cnpj='12.345.678/0001-90'
            )


class ProductModelTest(TestCase):
    """Testes para o modelo Product"""
    
    def setUp(self):
        """Prepara dados para os testes"""
        self.categoria = Category.objects.create(nome='Teste')
        self.produto = Product.objects.create(
            codigo='PROD-0001',
            nome='Produto Teste',
            categoria=self.categoria,
            unidade='UN',
            quantidade_estoque=Decimal('100.00'),
            custo_unitario=Decimal('50.00')
        )
    
    def test_produto_criacao(self):
        """Testa a criação de um produto"""
        self.assertEqual(self.produto.nome, 'Produto Teste')
        self.assertEqual(self.produto.codigo, 'PROD-0001')
        self.assertEqual(self.produto.categoria, self.categoria)
        self.assertEqual(self.produto.quantidade_estoque, Decimal('100.00'))
        self.assertEqual(self.produto.custo_unitario, Decimal('50.00'))
    
    def test_produto_str_com_codigo(self):
        """Testa a representação em string com código"""
        self.assertEqual(str(self.produto), 'PROD-0001 - Produto Teste')
    
    def test_produto_str_sem_codigo(self):
        """Testa a representação em string sem código (SKU é gerado automaticamente)"""
        produto_sem_codigo = Product.objects.create(
            nome='Produto Sem Código',
            categoria=self.categoria
        )
        # O SKU é gerado automaticamente, então deve começar com PROD-
        self.assertIsNotNone(produto_sem_codigo.codigo)
        self.assertTrue(str(produto_sem_codigo).startswith('PROD-'))
        self.assertIn('Produto Sem Código', str(produto_sem_codigo))
    
    def test_produto_valor_total_estoque(self):
        """Testa o cálculo do valor total do estoque"""
        valor_esperado = Decimal('100.00') * Decimal('50.00')
        self.assertEqual(self.produto.valor_total_estoque, valor_esperado)
    
    def test_produto_gera_sku_automatico(self):
        """Testa a geração automática de SKU"""
        produto_novo = Product.objects.create(
            nome='Produto Novo',
            categoria=self.categoria
        )
        self.assertIsNotNone(produto_novo.codigo)
        self.assertTrue(produto_novo.codigo.startswith('PROD-'))
    
    def test_produto_unique_codigo(self):
        """Testa que o código do produto deve ser único"""
        with self.assertRaises(Exception):
            Product.objects.create(
                codigo='PROD-0001',
                nome='Produto Duplicado',
                categoria=self.categoria
            )
    
    def test_produto_generate_sku(self):
        """Testa o método estático de geração de SKU"""
        # Gera primeiro SKU
        sku1 = Product.generate_sku()
        self.assertTrue(sku1.startswith('PROD-'))
        
        # Cria produto com SKU
        Product.objects.create(
            codigo=sku1,
            nome='Produto 1',
            categoria=self.categoria
        )
        
        # Gera próximo SKU
        sku2 = Product.generate_sku()
        self.assertNotEqual(sku1, sku2)
        self.assertTrue(sku2.startswith('PROD-'))


class StockMovementModelTest(TestCase):
    """Testes para o modelo StockMovement"""
    
    def setUp(self):
        """Prepara dados para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.categoria = Category.objects.create(nome='Teste')
        self.fornecedor = Supplier.objects.create(nome='Fornecedor Teste')
        self.produto = Product.objects.create(
            codigo='PROD-0001',
            nome='Produto Teste',
            categoria=self.categoria,
            quantidade_estoque=Decimal('100.00'),
            custo_unitario=Decimal('50.00')
        )
    
    def test_movimentacao_entrada_criacao(self):
        """Testa a criação de uma movimentação de entrada"""
        movimentacao = StockMovement.objects.create(
            tipo='ENTRADA',
            produto=self.produto,
            quantidade=Decimal('50.00'),
            custo_unitario=Decimal('60.00'),
            fornecedor=self.fornecedor,
            usuario=self.user
        )
        
        self.assertEqual(movimentacao.tipo, 'ENTRADA')
        self.assertEqual(movimentacao.produto, self.produto)
        self.assertEqual(movimentacao.quantidade, Decimal('50.00'))
        self.assertEqual(movimentacao.fornecedor, self.fornecedor)
        self.assertEqual(movimentacao.usuario, self.user)
    
    def test_movimentacao_entrada_atualiza_estoque(self):
        """Testa que uma entrada atualiza o estoque do produto"""
        estoque_inicial = self.produto.quantidade_estoque
        
        StockMovement.objects.create(
            tipo='ENTRADA',
            produto=self.produto,
            quantidade=Decimal('25.00'),
            custo_unitario=Decimal('60.00'),
            fornecedor=self.fornecedor,
            usuario=self.user
        )
        
        # Recarrega o produto do banco
        self.produto.refresh_from_db()
        
        estoque_final = self.produto.quantidade_estoque
        self.assertEqual(estoque_final, estoque_inicial + Decimal('25.00'))
    
    def test_movimentacao_saida_atualiza_estoque(self):
        """Testa que uma saída atualiza o estoque do produto"""
        estoque_inicial = self.produto.quantidade_estoque
        
        StockMovement.objects.create(
            tipo='SAIDA',
            produto=self.produto,
            quantidade=Decimal('30.00'),
            usuario=self.user
        )
        
        # Recarrega o produto do banco
        self.produto.refresh_from_db()
        
        estoque_final = self.produto.quantidade_estoque
        self.assertEqual(estoque_final, estoque_inicial - Decimal('30.00'))
    
    def test_movimentacao_entrada_atualiza_custo_medio(self):
        """Testa que uma entrada atualiza o custo médio ponderado"""
        custo_inicial = self.produto.custo_unitario
        
        StockMovement.objects.create(
            tipo='ENTRADA',
            produto=self.produto,
            quantidade=Decimal('100.00'),
            custo_unitario=Decimal('60.00'),
            fornecedor=self.fornecedor,
            usuario=self.user
        )
        
        # Recarrega o produto do banco
        self.produto.refresh_from_db()
        
        # Verifica que o custo foi atualizado (média ponderada)
        self.assertNotEqual(self.produto.custo_unitario, custo_inicial)
    
    def test_movimentacao_str(self):
        """Testa a representação em string da movimentação"""
        movimentacao = StockMovement.objects.create(
            tipo='ENTRADA',
            produto=self.produto,
            quantidade=Decimal('10.00'),
            usuario=self.user
        )
        
        self.assertIn('Entrada', str(movimentacao))
        self.assertIn(self.produto.nome, str(movimentacao))
        self.assertIn('10.00', str(movimentacao))
    
    def test_movimentacao_nao_permitir_quantidade_zero(self):
        """Testa que não é permitido criar movimentação com quantidade zero"""
        # O modelo usa MinValueValidator(Decimal('0.01')), então deve validar
        from django.core.exceptions import ValidationError
        from django.db import IntegrityError
        
        try:
            movimentacao = StockMovement(
                tipo='ENTRADA',
                produto=self.produto,
                quantidade=Decimal('0.00'),
                usuario=self.user
            )
            movimentacao.full_clean()  # Dispara validação
            # Se passar, tenta salvar (pode falhar no banco)
            try:
                movimentacao.save()
                self.fail("Deveria ter falhado ao criar movimentação com quantidade zero")
            except (ValidationError, IntegrityError, ValueError):
                pass  # Esperado
        except ValidationError:
            pass  # Esperado - validação funciona
    
    def test_multiplas_movimentacoes_estoque_final(self):
        """Testa múltiplas movimentações e verifica estoque final"""
        # Entrada 1
        StockMovement.objects.create(
            tipo='ENTRADA',
            produto=self.produto,
            quantidade=Decimal('50.00'),
            custo_unitario=Decimal('60.00'),
            fornecedor=self.fornecedor,
            usuario=self.user
        )
        
        # Saída 1
        StockMovement.objects.create(
            tipo='SAIDA',
            produto=self.produto,
            quantidade=Decimal('20.00'),
            usuario=self.user
        )
        
        # Entrada 2
        StockMovement.objects.create(
            tipo='ENTRADA',
            produto=self.produto,
            quantidade=Decimal('30.00'),
            custo_unitario=Decimal('70.00'),
            fornecedor=self.fornecedor,
            usuario=self.user
        )
        
        # Recarrega o produto
        self.produto.refresh_from_db()
        
        # Estoque esperado: 100 + 50 - 20 + 30 = 160
        self.assertEqual(self.produto.quantidade_estoque, Decimal('160.00'))

