# 📦 Guia de Deploy para Produção - Stockbit

Este documento contém as instruções para fazer o deploy do Stockbit em produção.

## 🔧 Pré-requisitos

- Docker e Docker Compose instalados no servidor
- Domínio ou IP configurado
- Acesso SSH ao servidor

## 📋 Passo a Passo para Deploy

### 1. Clonar o Repositório

```bash
git clone <repository-url>
cd Stockbit
```

### 2. Configurar Variáveis de Ambiente

Copie o arquivo de exemplo e configure as variáveis:

```bash
cp env.production.example .env
```

Edite o arquivo `.env` com suas configurações:

```env
# Django Settings
SECRET_KEY=sua-chave-secreta-muito-forte-aqui-minimo-50-caracteres
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com

# Database
DB_NAME=stockbit_db
DB_USER=stockbit_user
DB_PASSWORD=senha-forte-para-banco-de-dados

# CORS Settings
CORS_ALLOWED_ORIGINS=https://seudominio.com,https://www.seudominio.com

# API Settings
VITE_API_URL=https://seudominio.com/api

# Security Settings (habilite se usar HTTPS)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 3. Realizar o Build

```bash
docker-compose -f docker-compose.prod.yml build
```

### 4. Iniciar os Serviços

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### 5. Criar Superusuário (se necessário)

```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

### 6. Verificar Logs

```bash
# Ver logs de todos os serviços
docker-compose -f docker-compose.prod.yml logs -f

# Ver logs de um serviço específico
docker-compose -f docker-compose.prod.yml logs -f backend
```

## 🔄 Comandos Úteis

### Reiniciar Serviços

```bash
docker-compose -f docker-compose.prod.yml restart
```

### Parar Serviços

```bash
docker-compose -f docker-compose.prod.yml stop
```

### Parar e Remover Containers

```bash
docker-compose -f docker-compose.prod.yml down
```

### Verificar Status

```bash
docker-compose -f docker-compose.prod.yml ps
```

### Atualizar o Sistema

```bash
# Atualizar código
git pull

# Reconstruir imagens
docker-compose -f docker-compose.prod.yml build

# Reiniciar serviços
docker-compose -f docker-compose.prod.yml up -d
```

## 🗄️ Backup do Banco de Dados

### Backup

```bash
docker-compose -f docker-compose.prod.yml exec db pg_dump -U stockbit_user stockbit_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore

```bash
cat backup.sql | docker-compose -f docker-compose.prod.yml exec -T db psql -U stockbit_user stockbit_db
```

## 🔐 Configuração SSL/HTTPS (opcional)

Para usar HTTPS, você pode usar o Nginx como proxy reverso e Let's Encrypt:

1. Instale o Nginx no servidor host
2. Configure um certificado SSL com Let's Encrypt (certbot)
3. Configure o Nginx como proxy reverso
4. Ative as configurações de segurança no `.env`

## 🚨 Troubleshooting

### Erro de Permissão no Banco de Dados

```bash
# Verificar logs do banco
docker-compose -f docker-compose.prod.yml logs db

# Resetar banco (CUIDADO: apaga todos os dados)
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d
```

### Erro de Conexão entre Frontend e Backend

Verifique se:
1. O `CORS_ALLOWED_ORIGINS` está configurado corretamente
2. As redes Docker estão configuradas
3. Os serviços estão na mesma rede

### Limpar Cache do Frontend

```bash
# Reconstruir apenas o frontend
docker-compose -f docker-compose.prod.yml build --no-cache frontend
docker-compose -f docker-compose.prod.yml up -d frontend
```

## 📊 Monitoramento

### Uso de Recursos

```bash
docker stats
```

### Acessar Shell do Container

```bash
# Backend
docker-compose -f docker-compose.prod.yml exec backend sh

# Frontend
docker-compose -f docker-compose.prod.yml exec frontend sh

# Database
docker-compose -f docker-compose.prod.yml exec db psql -U stockbit_user stockbit_db
```

## 🔒 Segurança

- ✅ Nunca commite o arquivo `.env`
- ✅ Use senhas fortes
- ✅ Mantenha DEBUG=False em produção
- ✅ Configure ALLOWED_HOSTS corretamente
- ✅ Use HTTPS em produção
- ✅ Mantenha o sistema atualizado
- ✅ Faça backups regulares

## 📞 Suporte

Em caso de problemas, verifique:
1. Os logs dos serviços
2. A configuração do `.env`
3. A conectividade da rede
4. Os recursos do servidor

