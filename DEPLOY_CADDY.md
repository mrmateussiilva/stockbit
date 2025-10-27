# 🚀 Deploy com Caddy - Stockbit

O Caddy é um servidor web moderno que gerencia automaticamente certificados SSL/HTTPS via Let's Encrypt, tornando o deploy em produção muito mais simples.

## 🔧 Pré-requisitos

- Docker e Docker Compose
- Domínio apontando para o IP do servidor
- Portas 80 e 443 liberadas no firewall

## 📋 Passo a Passo

### 1. Configurar o Domínio

Edite o arquivo `Caddyfile` e substitua `seu-domínio.com` pelo seu domínio real:

```caddy
meusite.com {
    # ... configurações ...
}
```

### 2. Configurar Variáveis de Ambiente

Copie e configure o arquivo `.env`:

```bash
cp env.production.example .env
nano .env
```

Configurações importantes:

```env
# Django Settings
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=meusite.com,www.meusite.com

# Database
DB_NAME=stockbit_db
DB_USER=stockbit_user
DB_PASSWORD=senha-forte

# CORS - Use HTTPS com o domínio configurado
CORS_ALLOWED_ORIGINS=https://meusite.com,https://www.meusite.com

# API URL - Use HTTPS
VITE_API_URL=https://meusite.com/api
```

### 3. Fazer o Build e Iniciar

```bash
# Build das imagens
docker-compose -f docker-compose.prod-caddy.yml build

# Iniciar serviços
docker-compose -f docker-compose.prod-caddy.yml up -d
```

### 4. Verificar Logs

```bash
# Logs de todos os serviços
docker-compose -f docker-compose.prod-caddy.yml logs -f

# Logs apenas do Caddy
docker-compose -f docker-compose.prod-caddy.yml logs -f caddy
```

### 5. Criar Superusuário

```bash
docker-compose -f docker-compose.prod-caddy.yml exec backend python manage.py createsuperuser
```

### 6. Aplicar Migrações

```bash
docker-compose -f docker-compose.prod-caddy.yml exec backend python manage.py migrate
```

## 🔐 HTTPS Automático

O Caddy automaticamente:
- ✅ Solicita e renova certificados SSL da Let's Encrypt
- ✅ Redireciona HTTP para HTTPS
- ✅ Funciona com wildcards (*.meusite.com)
- ✅ Renova certificados automaticamente

**Primeira vez:** Pode levar alguns minutos para o Let's Encrypt validar seu domínio.

## 📁 Estrutura de URLs

Com o Caddy configurado, a estrutura é:

- **Frontend:** `https://meusite.com`
- **API:** `https://meusite.com/api`
- **Admin Django:** `https://meusite.com/api/admin`
- **Arquivos Estáticos:** `https://meusite.com/static/`
- **Media Files:** `https://meusite.com/media/`

## 🔄 Comandos Úteis

### Ver Status
```bash
docker-compose -f docker-compose.prod-caddy.yml ps
```

### Reiniciar Serviços
```bash
docker-compose -f docker-compose.prod-caddy.yml restart
```

### Ver Logs do Caddy
```bash
docker-compose -f docker-compose.prod-caddy.yml logs caddy
```

### Parar Serviços
```bash
docker-compose -f docker-compose.prod-caddy.yml stop
```

### Parar e Remover Tudo
```bash
docker-compose -f docker-compose.prod-caddy.yml down
```

### Atualizar Sistema
```bash
git pull
docker-compose -f docker-compose.prod-caddy.yml build
docker-compose -f docker-compose.prod-caddy.yml up -d
```

## 🗄️ Backup do Banco de Dados

### Fazer Backup
```bash
docker-compose -f docker-compose.prod-caddy.yml exec db pg_dump -U stockbit_user stockbit_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restaurar Backup
```bash
cat backup.sql | docker-compose -f docker-compose.prod-caddy.yml exec -T db psql -U stockbit_user stockbit_db
```

## ⚙️ Configurações Avançadas do Caddy

### Adicionar Múltiplos Domínios

```caddy
meusite.com, www.meusite.com {
    # ... configurações ...
}
```

### Usar Email para Notificações

```caddy
meusite.com {
    # Caddy vai usar este email para notificações do Let's Encrypt
    email admin@meusite.com
    
    # ... configurações ...
}
```

### Customizar Logs

```caddy
meusite.com {
    log {
        level INFO
        output file /var/log/caddy/access.log {
            roll_size 100mb
            roll_keep 10
        }
        format json
    }
    
    # ... configurações ...
}
```

### Rate Limiting (Prevenir DDoS)

```caddy
rate_limit {
    zone dynamic {
        max_size 100
        ttl 10m
    }
}

meusite.com {
    rate_limit {
        zone dynamic
        requests 100
        window 1m
    }
    
    # ... configurações ...
}
```

## 🚨 Troubleshooting

### Certificado SSL não está sendo gerado

1. Verifique se o domínio está apontando para o servidor:
   ```bash
   nslookup meusite.com
   ```

2. Verifique se as portas 80 e 443 estão abertas:
   ```bash
   sudo ufw status
   ```

3. Verifique logs do Caddy:
   ```bash
   docker-compose -f docker-compose.prod-caddy.yml logs caddy
   ```

### Erro "Too Many Redirects"

Verifique se o `VITE_API_URL` no `.env` usa HTTPS:
```env
VITE_API_URL=https://meusite.com/api
```

### Erro de CORS

Verifique se o `CORS_ALLOWED_ORIGINS` no `.env` usa HTTPS:
```env
CORS_ALLOWED_ORIGINS=https://meusite.com,https://www.meusite.com
```

## 📊 Monitoramento

### Stats em Tempo Real
```bash
docker stats
```

### Ver Logs em Tempo Real
```bash
docker-compose -f docker-compose.prod-caddy.yml logs -f
```

### Acessar Admin do Caddy
```bash
docker-compose -f docker-compose.prod-caddy.yml exec caddy caddy admin
```

## 🔒 Segurança

- ✅ Certificados SSL renovados automaticamente
- ✅ Headers de segurança configurados
- ✅ Compressão gzip e zstd ativadas
- ✅ Rate limiting disponível (opcional)
- ✅ Logs estruturados em JSON

## 📚 Mais Informações

- [Documentação do Caddy](https://caddyserver.com/docs/)
- [Configuração de Proxy Reverso](https://caddyserver.com/docs/caddyfile/directives/reverse_proxy)
- [Automatic HTTPS](https://caddyserver.com/docs/automatic-https)

