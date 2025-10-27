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

### 🚀 Desenvolvimento com Docker (Recomendado)

1. Clone o repositório:
```bash
git clone <repository-url>
cd Stockbit
```

2. Execute o script de desenvolvimento:
```bash
./dev.sh start
```

3. Acesse a aplicação:
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000

### 📋 Comandos Disponíveis

```bash
./dev.sh start     # Inicia todos os serviços
./dev.sh stop      # Para os serviços
./dev.sh restart   # Reinicia os serviços
./dev.sh build     # Reconstrói as imagens
./dev.sh logs      # Mostra os logs
./dev.sh frontend  # Apenas o frontend
./dev.sh backend   # Apenas o backend
./dev.sh clean     # Remove containers e volumes
./dev.sh help      # Mostra ajuda
```

### 🔧 Configuração Manual

1. Configure as variáveis de ambiente (opcional):
```bash
cp docker.env.example .env
# Edite o arquivo .env conforme necessário
```

2. Execute com docker-compose:
```bash
docker-compose up --build
```

### 🎨 Componentes Modernos

O sistema agora inclui componentes modernos estilo shadcn/ui:
- ✅ Design system completo
- ✅ Componentes polidos e acessíveis
- ✅ Animações e micro-interações
- ✅ Tema claro/escuro
- ✅ PWA (Progressive Web App)
- ✅ Mobile-first design

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
