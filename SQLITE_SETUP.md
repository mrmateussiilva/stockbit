# Setup com SQLite (Simplificado)

Este guia mostra como configurar o Stockbit em produção usando SQLite ao invés de PostgreSQL.

## Vantagens do SQLite
- ✅ Mais simples - não precisa de container separado
- ✅ Zero configuração de banco de dados
- ✅ Ideal para começar rapidamente
- ✅ Perfeito para pequenas/médias aplicações
- ⚠️ Limitações: não recomendado para alta concorrência (muitos usuários simultâneos)

## Passo a Passo

### 1. Criar arquivo .env

No servidor, execute:

```bash
cd /opt/finderbit/stockbit
bash create-env.sh
```

Ou crie manualmente:

```bash
cat > .env << 'EOF'
# Django Settings
SECRET_KEY=ALTERE_AQUI_SUA_CHAVE_SECRETA_MIN_50_CARACTERES
DEBUG=False
ALLOWED_HOSTS=stockbit.finderbit.com.br,finderbit.com.br,localhost,127.0.0.1,caddy

# CORS Settings
CORS_ALLOWED_ORIGINS=https://stockbit.finderbit.com.br,https://finderbit.com.br

# API Settings
VITE_API_URL=https://stockbit.finderbit.com.br/api

# Security Settings
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True

# Timezone
TIME_ZONE=America/Sao_Paulo
EOF
```

### 2. Subir os containers

```bash
docker-compose -f docker-compose.prod-caddy-sqlite.yml up -d --build
```

### 3. Verificar os logs

```bash
# Ver logs do backend
docker-compose -f docker-compose.prod-caddy-sqlite.yml logs -f backend

# Ver logs do frontend
docker-compose -f docker-compose.prod-caddy-sqlite.yml logs -f frontend

# Ver logs do Caddy
docker-compose -f docker-compose.prod-caddy-sqlite.yml logs -f caddy
```

### 4. Fazer backup do banco SQLite

```bash
# Entrar no container
docker-compose -f docker-compose.prod-caddy-sqlite.yml exec backend bash

# Dentro do container
ls -lh /app/db.sqlite3

# Fazer backup
cp /app/db.sqlite3 /app/db.sqlite3.backup

# Sair do container
exit
```

### 5. Backup periódico (opcional)

Crie um script de backup:

```bash
cat > backup-sqlite.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker cp stockbit-backend-1:/app/db.sqlite3 /backup/db_${DATE}.sqlite3
echo "Backup realizado: db_${DATE}.sqlite3"
EOF

chmod +x backup-sqlite.sh
```

## Comandos Úteis

### Ver status
```bash
docker-compose -f docker-compose.prod-caddy-sqlite.yml ps
```

### Parar tudo
```bash
docker-compose -f docker-compose.prod-caddy-sqlite.yml down
```

### Reiniciar um serviço
```bash
docker-compose -f docker-compose.prod-caddy-sqlite.yml restart backend
```

### Ver logs em tempo real
```bash
docker-compose -f docker-compose.prod-caddy-sqlite.yml logs -f
```

## Migrar para PostgreSQL depois

Se precisar de mais performance ou concorrência, pode migrar para PostgreSQL usando o arquivo `docker-compose.prod-caddy.yml` original.

## Estrutura de Volumes

- `static_files`: Arquivos estáticos (CSS, JS, imagens)
- `media_files`: Uploads de usuários
- `sqlite_data`: Banco de dados SQLite (persiste)
- `caddy_data`: Certificados SSL
- `caddy_config`: Configuração do Caddy
- `caddy_logs`: Logs do Caddy

## Credenciais de Acesso

O usuário admin é criado **automaticamente** na primeira execução:

- **Username:** `finderbit`
- **Password:** `finderbit3010`
- **Email:** `admin@finderbit.com.br`

**⚠️ IMPORTANTE:** Altere a senha após o primeiro login por segurança!

## Verificações

1. ✅ DNS configurado para `stockbit.finderbit.com.br`
2. ✅ Portas 80 e 443 abertas no firewall
3. ✅ Arquivo `.env` criado
4. ✅ Container rodando: `docker-compose ps`
5. ✅ Acessar: `https://stockbit.finderbit.com.br`
6. ✅ Login admin: `https://stockbit.finderbit.com.br` com usuário `finderbit`
