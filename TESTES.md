# 🧪 Testes do StockBit

Documentação completa sobre os testes do sistema StockBit.

## 📋 Estrutura de Testes

Os testes estão organizados em módulos dentro de `estoque/tests/`:

```
estoque/tests/
├── __init__.py
├── test_models.py        # Testes dos modelos (Category, Supplier, Product, StockMovement)
├── test_forms.py         # Testes dos formulários (ProductForm, CategoryForm, SupplierForm, etc.)
├── test_views.py         # Testes das views (CRUD, APIs, autenticação)
└── test_integration.py   # Testes de integração end-to-end
```

## 🚀 Como Executar os Testes

### Executar Todos os Testes

```bash
python manage.py test
```

### Executar com Cobertura

```bash
# Instalar coverage se ainda não tiver
pip install coverage

# Executar testes com cobertura
make test-coverage
# ou
coverage run --source='.' manage.py test estoque
coverage report
coverage html
```

### Executar Grupos Específicos

```bash
# Apenas testes de modelos
make test-models
# ou
python manage.py test estoque.tests.test_models

# Apenas testes de views
make test-views
# ou
python manage.py test estoque.tests.test_views

# Apenas testes de formulários
make test-forms
# ou
python manage.py test estoque.tests.test_forms

# Apenas testes de integração
make test-integration
# ou
python manage.py test estoque.tests.test_integration
```

### Executar Teste Específico

```bash
python manage.py test estoque.tests.test_models.ProductModelTest
python manage.py test estoque.tests.test_models.ProductModelTest.test_produto_criacao
```

### Modo Verboso

```bash
python manage.py test --verbosity=2
```

## 📊 Tipos de Testes

### 1. Testes de Modelos (`test_models.py`)

Testam a funcionalidade dos modelos Django:

- **CategoryModelTest**: Criação, unicidade, representação em string
- **SupplierModelTest**: Criação, CNPJ único, representação
- **ProductModelTest**: 
  - Criação de produtos
  - Geração automática de SKU
  - Cálculo de valor total do estoque
  - Unicidade de código
- **StockMovementModelTest**:
  - Criação de movimentações
  - Atualização automática de estoque
  - Cálculo de custo médio ponderado
  - Validação de quantidade mínima

**Exemplo:**
```python
def test_produto_gera_sku_automatico(self):
    """Testa a geração automática de SKU"""
    produto_novo = Product.objects.create(
        nome='Produto Novo',
        categoria=self.categoria
    )
    self.assertIsNotNone(produto_novo.codigo)
    self.assertTrue(produto_novo.codigo.startswith('PROD-'))
```

### 2. Testes de Formulários (`test_forms.py`)

Testam validação e comportamento dos formulários:

- **ProductFormTest**: Validação de campos obrigatórios, SKU opcional
- **CategoryFormTest**: Criação de categorias
- **SupplierFormTest**: Validação de CNPJ, telefone, email
- **EntradaManualFormTest**: Criação de entradas
- **SaidaFormTest**: Validação de quantidade vs estoque disponível

**Exemplo:**
```python
def test_saida_form_quantidade_maior_que_estoque(self):
    """Testa validação quando quantidade excede estoque"""
    form_data = {
        'produto': self.produto.id,
        'quantidade': '150.00'  # Maior que o estoque (100.00)
    }
    form = SaidaForm(data=form_data)
    self.assertFalse(form.is_valid())
    self.assertIn('quantidade', form.errors)
```

### 3. Testes de Views (`test_views.py`)

Testam as views HTTP do sistema:

- **LoginViewTest**: Autenticação, redirecionamentos
- **DashboardViewTest**: Estatísticas do dashboard
- **ProductViewsTest**: CRUD completo de produtos
- **CategoryViewsTest**: CRUD de categorias
- **SupplierViewsTest**: CRUD de fornecedores
- **StockMovementViewsTest**: Entradas e saídas
- **APITests**: APIs JSON (estoque, verificação de SKU)

**Exemplo:**
```python
def test_produto_criar_post(self):
    """Testa criação de produto via POST"""
    response = self.client.post(reverse('estoque:produto_criar'), {
        'nome': 'Novo Produto',
        'categoria': self.categoria.id,
        'unidade': 'UN',
        'quantidade_estoque': '50.00',
        'custo_unitario': '30.00'
    })
    self.assertEqual(response.status_code, 302)  # Redirect
    self.assertTrue(Product.objects.filter(nome='Novo Produto').exists())
```

### 4. Testes de Integração (`test_integration.py`)

Testam fluxos completos end-to-end:

- **fluxo_completo_produto**: Criar categoria → fornecedor → produto → entrada → saída
- **fluxo_busca_e_filtros**: Busca e filtros de produtos
- **fluxo_multiplas_entradas_e_saidas**: Cálculo correto com múltiplas operações
- **fluxo_dashboard_estatisticas**: Estatísticas após operações
- **fluxo_edicao_produto_com_movimentacoes**: Edição mantendo histórico
- **fluxo_delete_produto_com_movimentacoes**: Deleção com dependências

**Exemplo:**
```python
def test_fluxo_completo_produto(self):
    """
    Testa fluxo completo: criar categoria -> criar fornecedor -> 
    criar produto -> fazer entrada -> fazer saída -> verificar estoque
    """
    # 1. Criar categoria
    # 2. Criar fornecedor
    # 3. Criar produto
    # 4. Fazer entrada
    # 5. Fazer saída
    # 6. Verificar estoque final
```

## 🔧 Configuração

### Requisitos

Adicione ao `requirements.txt`:

```txt
coverage>=7.0.0
```

Instale:

```bash
pip install -r requirements.txt
```

### Cobertura de Código

O arquivo `.coveragerc` configura:

- Fontes a cobrir: apenas `estoque`
- Arquivos omitidos: migrations, tests, __pycache__
- Precisão: 2 casas decimais
- Relatório HTML em `htmlcov/`

## 📈 Interpretando Resultados

### Saída de Testes Bem-Sucedidos

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.........
----------------------------------------------------------------------
Ran 10 tests in 0.123s

OK
Destroying test database for alias 'default'...
```

### Saída de Cobertura

```
Name                      Stmts   Miss  Cover
---------------------------------------------
estoque/models.py           120      5    96%
estoque/views.py            250     15    94%
estoque/forms.py             80      2    98%
---------------------------------------------
TOTAL                       450     22    95%
```

## 🐛 Resolução de Problemas

### Teste Falhando

1. **Verificar mensagem de erro**:
   ```bash
   python manage.py test --verbosity=2 estoque.tests.test_models
   ```

2. **Verificar se dados estão corretos**:
   - Verifique `setUp()` do teste
   - Verifique se o modelo/fomulário foi alterado

3. **Verificar dependências**:
   - Migrations aplicadas?
   - Fixtures carregadas?

### Banco de Teste

O Django cria um banco de dados de teste automaticamente. Para forçar recriação:

```bash
python manage.py test --keepdb  # Mantém banco entre execuções
python manage.py test            # Recria banco a cada execução
```

## ✅ Boas Práticas

1. **Um teste, uma coisa**: Cada teste deve verificar uma funcionalidade específica
2. **Nomes descritivos**: Use nomes que expliquem o que o teste faz
3. **Dados isolados**: Use `setUp()` para dados de teste, não compartilhe estado
4. **Limpeza**: O Django limpa automaticamente, mas evite efeitos colaterais
5. **Asserções claras**: Use mensagens descritivas nas asserções

**Exemplo:**
```python
def test_produto_valor_total_estoque(self):
    """Testa o cálculo do valor total do estoque"""
    valor_esperado = Decimal('100.00') * Decimal('50.00')
    self.assertEqual(
        self.produto.valor_total_estoque,
        valor_esperado,
        msg="Valor total do estoque deve ser quantidade × custo unitário"
    )
```

## 🔄 CI/CD

### GitHub Actions (exemplo)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.12
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python manage.py test
      - name: Generate coverage
        run: |
          coverage run --source='.' manage.py test estoque
          coverage xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## 📚 Referências

- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Test-Driven Development](https://testdriven.io/)

