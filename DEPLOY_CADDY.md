# 🚀 Deploy StockBit com Caddy

Este guia mostra como fazer deploy do StockBit usando Docker e Caddy como reverse proxy.

## 📋 Pré-requisitos

- VPS com Docker e Docker Compose instalados
- Caddy instalado e rodando
- Domínio apontando para seu servidor
- Pelo menos 2GB de RAM disponível

## 🔧 Configuração

### 1. Clone e Configure o Projeto

```bash
# Clone o repositório
git clone seu-repositorio stockbit
cd stockbit

# Configure as variáveis de ambiente
cp .env.production.example .env.production
nano .env.production
```

Configure pelo menos:
```bash
DEBUG=False
SECRET_KEY=sua-chave-secreta-super-segura-aqui
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com
POSTGRES_PASSWORD=senha_super_segura_altere_isso
```

### 2. Construa e Inicie os Containers

```bash
# Construa as imagens
docker-compose -f docker-compose.simple.yml build

# Inicie os serviços (detached mode)
docker-compose -f docker-compose.simple.yml up -d

# Verifique se estão rodando
docker-compose -f docker-compose.simple.yml ps

# Veja os logs
docker-compose -f docker-compose.simple.yml logs -f
```

### 3. Configure o Caddy

```bash
# Copie o exemplo do Caddyfile
cp Caddyfile.example Caddyfile

# Edite o Caddyfile
nano Caddyfile
```

Configure seu domínio:
```
seu-dominio.com {
    reverse_proxy localhost:8000
    
    tls {
        protocols tls1.2 tls1.3
    }
}
```

**OU** adicione ao seu Caddyfile existente:

```caddy
# Configuração para StockBit
seu-dominio.com {
    reverse_proxy localhost:8000
    
    # Headers de segurança
    header {
        X-Content-Type-Options "nosniff"
        X-Frame-Options "SAMEORIGIN"
        X-XSS-Protection "1; mode=block"
    }
    
    # Compressão
    encode gzip zstd
    
    # TLS automático
    tls {
        protocols tls1.2 tls1.3
    }
}
```

### 4. Recarregue o Caddy

```bash
# Recarregue a configuração do Caddy
sudo caddy reload --config /etc/caddy/Caddyfile

# OU se usar systemd
sudo systemctl reload caddy
```

### 5. Crie o Superusuário

```bash
docker-compose -f docker-compose.simple.yml exec web python manage.py createsuperuser
```

## 🔐 Segurança

### Configurações Importantes no .env.production

```bash
# Django
DEBUG=False
SECRET_KEY=chave-secreta-gerada
ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com

# Segurança (já configurado no Caddy)
SECURE_SSL_REDIRECT=False  # Caddy já redireciona HTTPS
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Firewall (Opcional mas Recomendado)

```bash
# Permite apenas SSH, HTTP e HTTPS
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

**Importante:** A porta 8000 NÃO precisa estar exposta externamente, apenas localmente para o Caddy.

## 📊 Gerenciamento

### Ver Status

```bash
# Status dos containers
docker-compose -f docker-compose.simple.yml ps

# Logs
docker-compose -f docker-compose.simple.yml logs -f web
docker-compose -f docker-compose.simple.yml logs -f db

# Status do Caddy
sudo systemctl status caddy
caddy version
```

### Backup do Banco

```bash
# Criar backup
docker-compose -f docker-compose.simple.yml exec db pg_dump -U stockbit stockbit > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar backup
docker-compose -f docker-compose.simple.yml exec -T db psql -U stockbit stockbit < backup.sql
```

### Atualizar a Aplicação

```bash
# Pare os containers
docker-compose -f docker-compose.simple.yml down

# Atualize o código
git pull

# Reconstrua e reinicie
docker-compose -f docker-compose.simple.yml build --no-cache
docker-compose -f docker-compose.simple.yml up -d

# Execute migrações (se necessário)
docker-compose -f docker-compose.simple.yml exec web python manage.py migrate
```

### Executar Comandos Django

```bash
# Shell do Django
docker-compose -f docker-compose.simple.yml exec web python manage.py shell

# Migrar
docker-compose -f docker-compose.simple.yml exec web python manage.py migrate

# Coletar estáticos
docker-compose -f docker-compose.simple.yml exec web python manage.py collectstatic

# Criar superusuário
docker-compose -f docker-compose.simple.yml exec web python manage.py createsuperuser
```

## 🐛 Troubleshooting

### Container não inicia

```bash
# Veja os logs detalhados
docker-compose -f docker-compose.simple.yml logs web

# Verifique se o banco está saudável
docker-compose -f docker-compose.simple.yml ps db

# Entre no container para debugar
docker-compose -f docker-compose.simple.yml exec web bash
```

### Caddy não consegue se conectar

1. Verifique se a porta 8000 está acessível:
```bash
curl http://localhost:8000
```

2. Verifique se o container está rodando:
```bash
docker ps | grep stockbit_web
```

3. Veja os logs do web:
```bash
docker-compose -f docker-compose.simple.yml logs web
```

### Erro de permissões

```bash
# Ajuste as permissões
sudo chown -R 1000:1000 ./staticfiles ./media
```

### Recursos de Sobercarga

```bash
# Ver uso de recursos
docker stats

# Se precisar, ajuste o número de workers no Dockerfile
# Linha: --workers 4 (diminua para 2 se tiver pouca RAM)
```

## 🔄 Configuração Automática no Caddy

### Múltiplos Domínios

```caddy
stockbit.empresa.com {
    reverse_proxy localhost:8000
    encode gzip zstd
    tls { protocols tls1.2 tls1.3 }
}

app.empresa.com {
    reverse_proxy localhost:8000
    encode gzip zstd
    tls { protocols tls1.2 tls1.3 }
}
```

### Rate Limiting (Proteção DDoS)

```caddy
seu-dominio.com {
    rate_limit {
        zone login {
            key {remote_host}
            events 5
            window 1m
        }
        zone general {
            key {remote_host}
            events 100
            window 1m
        }
    }
    
    reverse_proxy localhost:8000
}
```

## 📝 Scripts Úteis

### Criar script de backup automático

```bash
# Crie o script
nano backup_stockbit.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/backups/stockbit"
DATE=$(date +%Y%m%d_%H%M%S)

# Criar diretório se não existir
mkdir -p $BACKUP_DIR

# Backup do banco
docker-compose -f /path/to/stockbit/docker-compose.simple.yml exec -T db pg_dump -U stockbit stockbit > $BACKUP_DIR/db_$DATE.sql

# Backup dos arquivos de media
tar -czf $BACKUP_DIR/media_$DATE.tar.gz -C /path/to/stockbit/media .

# Manter apenas os últimos 7 backups
find $BACKUP_DIR -name "db_*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "media_*.tar.gz" -mtime +7 -delete

echo "Backup criado: $DATE"
```

```bash
chmod +x backup_stockbit.sh

# Adicione ao crontab
crontab -e

# Adicione a linha (backup diário às 2h da manhã)
0 2 * * * /path/to/backup_stockbit.sh
```

## ✅ Checklist de Deploy

- [ ] Docker e Docker Compose instalados
- [ ] Caddy instalado e configurado
- [ ] Domínio apontando para o servidor
- [ ] Arquivo .env.production configurado
- [ ] SECRET_KEY gerada e configurada
- [ ] POSTGRES_PASSWORD alterado
- [ ] ALLOWED_HOSTS configurado
- [ ] Containers construídos e rodando
- [ ] Caddyfile configurado
- [ ] Caddy recarregado
- [ ] Superusuário criado
- [ ] Aplicação acessível via HTTPS
- [ ] Backup configurado
- [ ] Firewall configurado
- [ ] Logs monitorados

## 🆘 Suporte

Em caso de problemas:

1. Verifique os logs do Docker: `docker-compose logs`
2. Verifique os logs do Caddy: `sudo journalctl -u caddy -f`
3. Teste a conectividade: `curl http://localhost:8000`
4. Verifique status dos containers: `docker ps`

