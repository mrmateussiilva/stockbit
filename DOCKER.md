# 🐳 Guia de Deploy com Docker - StockBit

Este guia explica como fazer o deploy do StockBit em produção usando Docker e PostgreSQL.

## 📋 Pré-requisitos

- Docker Engine 20.10+
- Docker Compose 2.0+
- Pelo menos 2GB de RAM disponível
- Portas 80, 443 e 5432 disponíveis

## 🚀 Início Rápido

### 1. Configure as Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.production.example .env.production

# Edite o arquivo com suas configurações
nano .env.production
```

**Importante:** Altere pelo menos:
- `SECRET_KEY` - Gere uma chave secreta única
- `POSTGRES_PASSWORD` - Senha segura para o banco
- `ALLOWED_HOSTS` - Domínio(s) onde o sistema estará disponível

Para gerar uma nova `SECRET_KEY`:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2. Construa e Inicie os Containers

```bash
# Construa as imagens
docker-compose build

# Inicie os serviços
docker-compose up -d

# Verifique os logs
docker-compose logs -f
```

### 3. Acesse a Aplicação

- **Aplicação:** http://localhost
- **Aplicação (diretamente):** http://localhost:8000

## 📦 Serviços

O `docker-compose.yml` cria 3 serviços:

1. **db** - PostgreSQL 16 (banco de dados)
2. **web** - Django + Gunicorn (aplicação)
3. **nginx** - Servidor web reverso (opcional, mas recomendado)

## 🔧 Configuração

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `DEBUG` | Modo debug | `False` |
| `SECRET_KEY` | Chave secreta Django | - |
| `ALLOWED_HOSTS` | Hosts permitidos | `localhost,127.0.0.1` |
| `POSTGRES_DB` | Nome do banco | `stockbit` |
| `POSTGRES_USER` | Usuário do banco | `stockbit` |
| `POSTGRES_PASSWORD` | Senha do banco | - |
| `POSTGRES_HOST` | Host do banco | `db` |
| `POSTGRES_PORT` | Porta do banco | `5432` |

### SSL/HTTPS

Para habilitar HTTPS:

1. Coloque seus certificados SSL em `./ssl/`:
   - `cert.pem` (certificado)
   - `key.pem` (chave privada)

2. Descomente as seções HTTPS no `nginx.conf`

3. Configure no `.env.production`:
   ```
   SECURE_SSL_REDIRECT=True
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   ```

## 🔐 Criar Superusuário

Para criar o primeiro usuário administrador:

```bash
docker-compose exec web python manage.py createsuperuser
```

Ou descomente a seção no `entrypoint.sh` (não recomendado para produção).

## 📊 Comandos Úteis

```bash
# Ver logs
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx

# Executar comandos Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
docker-compose exec web python manage.py createsuperuser

# Acessar shell do container
docker-compose exec web bash

# Parar serviços
docker-compose down

# Parar e remover volumes (CUIDADO: apaga dados!)
docker-compose down -v

# Reconstruir após mudanças
docker-compose build --no-cache
docker-compose up -d
```

## 🔄 Backup do Banco de Dados

```bash
# Backup
docker-compose exec db pg_dump -U stockbit stockbit > backup_$(date +%Y%m%d_%H%M%S).sql

# Restaurar
docker-compose exec -T db psql -U stockbit stockbit < backup.sql
```

## 📈 Monitoramento

### Logs

Os logs são salvos em:
- **Web:** Saída padrão (use `docker-compose logs`)
- **Nginx:** `/var/log/nginx/` (dentro do container)
- **PostgreSQL:** Saída padrão

### Health Checks

O PostgreSQL tem health check configurado. Verifique:

```bash
docker-compose ps
```

## 🛠️ Troubleshooting

### Erro de conexão com banco

```bash
# Verifique se o banco está rodando
docker-compose ps db

# Verifique os logs
docker-compose logs db

# Teste conexão
docker-compose exec web python manage.py dbshell
```

### Erro de permissões

```bash
# Ajuste permissões dos volumes
sudo chown -R 1000:1000 ./staticfiles ./media
```

### Reconstruir tudo

```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## 🔒 Segurança

- ✅ Use senhas fortes em produção
- ✅ Configure SSL/HTTPS
- ✅ Mantenha `DEBUG=False` em produção
- ✅ Configure `ALLOWED_HOSTS` corretamente
- ✅ Use secrets/vault para senhas em produção
- ✅ Mantenha imagens Docker atualizadas

## 📝 Notas

- Os volumes persistem dados mesmo após parar containers
- Use `docker-compose down -v` apenas se quiser apagar tudo
- Para produção real, considere usar Docker Swarm ou Kubernetes
- Configure backups automáticos do PostgreSQL

## 🆘 Suporte

Em caso de problemas:
1. Verifique os logs: `docker-compose logs`
2. Verifique as variáveis de ambiente: `.env.production`
3. Verifique a saúde dos containers: `docker-compose ps`

