# Stockbit - Sistema de Gestão de Estoque

Sistema moderno de gestão de estoque desenvolvido com Django REST Framework, React e TailwindCSS.

## 🚀 Tecnologias

- **Backend**: Python 3 + Django REST Framework
- **Frontend**: React + TailwindCSS
- **Banco de Dados**: MySQL 5.6 (remoto)
- **Autenticação**: JWT
- **Containerização**: Docker + Docker Compose

## 📦 Funcionalidades

- ✅ CRUD de produtos (nome, descrição, preço, quantidade, SKU, categoria)
- ✅ Controle de entradas e saídas
- ✅ Painel de resumo (quantidade total, produtos em baixa, movimentações recentes)
- ✅ Autenticação e controle de usuários
- ✅ Dashboard moderno e responsivo

## 🛠️ Instalação e Execução

### Pré-requisitos

- Docker
- Docker Compose
- Git

### Configuração Rápida

1. Clone o repositório
2. Execute o script de configuração:

```bash
./setup.sh
```

### Configuração Manual

1. Configure as variáveis de ambiente no arquivo `.env`:

```env
# Configurações do Banco de Dados MySQL (UOL Host)
DB_HOST=meubanco.uol.com.br
DB_PORT=3306
DB_NAME=estoque_db
DB_USER=usuario
DB_PASSWORD=senha

# Configurações do Django
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Configurações do Frontend
VITE_API_URL=http://localhost:8000/api
```

2. Execute os comandos:

```bash
# Subir os containers
make up

# Ou usando docker-compose diretamente
docker-compose up --build
```

### Acesso

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Admin Django**: http://localhost:8000/admin

### Credenciais Padrão

- **Usuário**: admin
- **Senha**: admin123

## 📁 Estrutura do Projeto

```
inventory-system/
├── backend/
│   ├── Dockerfile
│   ├── manage.py
│   ├── requirements.txt
│   ├── inventory_api/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   └── apps/
│       ├── users/
│       ├── products/
│       ├── stock/
│       └── dashboard/
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── tailwind.config.js
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── public/
└── docker-compose.yml
```

## 🔧 Comandos Make

```bash
make up      # Sobe os containers
make down    # Para os containers
make build   # Reconstrói os containers
make logs    # Visualiza logs
```

## 📊 API Endpoints

### Autenticação
- `POST /api/auth/login/` - Login
- `POST /api/auth/refresh/` - Refresh token
- `POST /api/auth/logout/` - Logout

### Produtos
- `GET /api/products/` - Listar produtos
- `POST /api/products/` - Criar produto
- `GET /api/products/{id}/` - Detalhar produto
- `PUT /api/products/{id}/` - Atualizar produto
- `DELETE /api/products/{id}/` - Deletar produto

### Estoque
- `GET /api/stock/movements/` - Listar movimentações
- `POST /api/stock/movements/` - Criar movimentação
- `GET /api/stock/summary/` - Resumo do estoque

### Dashboard
- `GET /api/dashboard/stats/` - Estatísticas gerais

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
