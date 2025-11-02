# StockBit - Sistema de Controle de Estoque

Sistema completo de controle de estoque desenvolvido com Django 5+ e Python, utilizando templates HTML nativos (sem frameworks JavaScript).

## 📦 Funcionalidades

### ✅ Cadastros
- **Produtos**: Código (SKU), Nome, Categoria, Unidade, Quantidade em Estoque, Custo Unitário, NCM, EAN
- **Categorias**: Organização de produtos por categoria
- **Fornecedores**: Cadastro de fornecedores (opcional)

### 📥 Entradas de Produtos
- **Entrada Manual**: Formulário para registrar entrada de produtos manualmente
- **Entrada via XML**: Upload de arquivo XML de NF-e (Nota Fiscal Eletrônica)
  - Extração automática de produtos do XML
  - Vinculação automática a produtos existentes (por código, NCM ou EAN)
  - Opção de criar novos produtos automaticamente

### 📤 Saídas de Produtos
- Formulário simples para registrar saída de produtos
- Validação automática de estoque disponível
- Histórico de movimentações

### 📊 Produtos
- Lista de produtos organizados por categoria
- Filtros por categoria e busca por nome/código/NCM
- Exportação para XLSX (Excel)

### 📈 Relatórios e Gráficos
- Gráfico de barras (Chart.js) mostrando uso de materiais por mês
- Filtro por período (data inicial/final)
- Resumo do estoque no período (Entradas, Saídas, Saldo Final)
- Exportação de relatórios para XLSX

## 🛠️ Stack Tecnológica

- **Django 5.0+**: Framework web
- **SQLite**: Banco de dados (pode ser trocado)
- **Bootstrap 5**: Framework CSS para interface
- **Chart.js**: Gráficos interativos
- **openpyxl**: Exportação para planilhas Excel
- **xml.etree.ElementTree**: Parsing de XML de NF-e
- **uv**: Gerenciador de ambiente virtual e pacotes

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.12+
- uv (https://github.com/astral-sh/uv)

### Passos

1. **Clone o repositório ou navegue até o diretório do projeto**

2. **Crie e ative o ambiente virtual (já criado)**
   ```bash
   uv venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .venv\Scripts\activate  # Windows
   ```

3. **Instale as dependências (já instaladas)**
   ```bash
   uv pip install django==5.0.2 openpyxl
   ```

4. **Execute as migrações (já executadas)**
   ```bash
   uv run python manage.py migrate
   ```

5. **Crie um superusuário**
   ```bash
   uv run python manage.py createsuperuser
   ```

6. **Execute o servidor de desenvolvimento**
   ```bash
   uv run python manage.py runserver
   ```

7. **Acesse o sistema**
   - Sistema: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## 📁 Estrutura do Projeto

```
stockBit/
├── estoque/                  # Aplicação principal
│   ├── models.py            # Modelos (Product, Category, Supplier, StockMovement)
│   ├── views.py             # Views de todas as funcionalidades
│   ├── forms.py             # Formulários Django
│   ├── urls.py              # URLs da aplicação
│   ├── admin.py             # Configuração do admin
│   ├── utils/               # Utilitários
│   │   ├── xml_parser.py    # Parser de XML de NF-e
│   │   └── export_xlsx.py   # Exportação para Excel
│   └── templates/           # Templates HTML
│       └── estoque/
│           ├── produtos/
│           ├── entradas/
│           ├── saidas/
│           └── relatorios/
├── stockbit/                # Configuração do projeto
│   ├── settings.py
│   └── urls.py
├── templates/               # Templates base
│   └── base.html
├── manage.py
└── README.md
```

## 🔐 Autenticação

O sistema utiliza autenticação padrão do Django. É necessário fazer login para acessar as funcionalidades.

## 📝 Uso Básico

### 1. Cadastrar Categorias
- Acesse o Admin Django (/admin/)
- Crie categorias em "Categorias"

### 2. Cadastrar Produtos
- Menu "Produtos" > "Novo Produto"
- Preencha os dados e salve

### 3. Registrar Entrada
- **Manual**: Menu "Entradas" > "Entrada Manual"
- **XML**: Menu "Entradas" > "Entrada via XML" > Envie o arquivo XML da NF-e

### 4. Registrar Saída
- Menu "Saídas"
- Selecione o produto e informe a quantidade
- O sistema valida o estoque disponível

### 5. Visualizar Relatórios
- Menu "Relatórios"
- Selecione o período
- Visualize gráficos e exporte para Excel

## 🔄 Fluxo de Entrada via XML

1. Faça upload do arquivo XML da NF-e
2. O sistema extrai os produtos automaticamente
3. Produtos encontrados no cadastro são vinculados automaticamente
4. Produtos não encontrados podem ser criados marcando a opção
5. Confirme para processar as entradas

## 📊 Relatórios

- **Gráfico de Uso**: Visualiza saídas de produtos por mês
- **Resumo**: Total de entradas, saídas e saldo final
- **Movimentações**: Tabela com todas as movimentações do período
- **Exportação**: Botão para exportar tudo para XLSX

## 🛡️ Segurança

- Autenticação obrigatória para todas as páginas
- Validação de estoque antes de saídas
- Histórico de movimentações com usuário responsável

## 📝 Notas

- O sistema calcula automaticamente o custo médio ponderado ao registrar entradas
- Produtos com estoque <= 5 são destacados como "estoque crítico"
- O parser XML suporta versões 3.10 e 4.00 do schema NF-e

## 🐛 Solução de Problemas

### Erro ao processar XML
- Verifique se o arquivo é um XML válido de NF-e
- Alguns campos podem não estar presentes dependendo da versão do schema

### Produtos não aparecem na saída
- Verifique se há quantidade em estoque
- Apenas produtos com estoque > 0 aparecem na lista de saída

## 📄 Licença

Este projeto é de uso interno.

## 👤 Autor

Sistema desenvolvido para controle de estoque.

