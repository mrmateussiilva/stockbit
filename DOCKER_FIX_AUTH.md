# 🔧 Correção de Autenticação PostgreSQL

## Problema Identificado

O erro `password authentication failed for user "stockbit"` ocorria porque:

1. **Lógica incorreta no `settings.py`**: Quando `DEBUG=True`, mesmo com variáveis PostgreSQL configuradas, usava SQLite
2. **Credenciais não sincronizadas**: Default diferente entre `settings.py` e `docker-compose.yml`
3. **Variáveis não passadas**: O container `web` não recebia as credenciais do PostgreSQL

## ✅ Correções Implementadas

### 1. Correção do `settings.py`

**Antes:**
```python
} if not DEBUG else {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        ...
    }
}
```

**Depois:**
```python
# Prioridade: DATABASE_URL > PostgreSQL env vars > SQLite (dev)
USE_POSTGRESQL = config('POSTGRES_HOST', default=None) or config('DATABASE_URL', default=None)

if config('DATABASE_URL', default=None):
    # Usa DATABASE_URL se disponível
elif USE_POSTGRESQL:
    # Usa PostgreSQL se variáveis estiverem definidas (independente de DEBUG)
    DATABASES = { ... PostgreSQL config ... }
else:
    # SQLite apenas quando PostgreSQL não está configurado
    DATABASES = { ... SQLite config ... }
```

**Mudanças:**
- Agora detecta PostgreSQL pela presença de `POSTGRES_HOST` ou `DATABASE_URL`
- Não depende mais de `DEBUG` para usar PostgreSQL
- Senha padrão sincronizada: `stockbit_password_change_me`

### 2. Correção do `docker-compose.simple.yml`

**Adicionado no container `web`:**
```yaml
environment:
  - POSTGRES_HOST=db
  - POSTGRES_PORT=5432
  - POSTGRES_DB=${POSTGRES_DB:-stockbit}
  - POSTGRES_USER=${POSTGRES_USER:-stockbit}
  - POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-stockbit_password_change_me}
```

**Resultado:**
- As credenciais são garantidamente passadas do host para o container `web`
- Usa as mesmas variáveis do container `db`
- Garante sincronização completa

### 3. Arquivo `.env.production.example`

Criado arquivo completo com todas as variáveis necessárias e valores padrão sincronizados.

## 🚀 Como Usar

### 1. Criar `.env.production`

```bash
cp .env.production.example .env.production
```

### 2. Editar `.env.production`

**IMPORTANTE:** As credenciais PostgreSQL devem ser **exatamente iguais** no `.env.production` e no `docker-compose.simple.yml`:

```bash
# .env.production
POSTGRES_DB=stockbit
POSTGRES_USER=stockbit
POSTGRES_PASSWORD=SUA_SENHA_SEGURA_AQUI

# docker-compose.simple.yml já usa as mesmas variáveis via ${POSTGRES_*}
```

### 3. Testar Conexão

```bash
# Executa testes de conexão
./scripts/test_postgres_connection.sh
```

O script verifica:
- ✅ Containers rodando
- ✅ Conexão do host (se psql instalado)
- ✅ Conexão do container web
- ✅ Conexão via Django

### 4. Deploy

```bash
# Parar containers existentes
docker-compose -f docker-compose.simple.yml down

# Subir com novas configurações
docker-compose -f docker-compose.simple.yml up -d

# Ver logs
docker-compose -f docker-compose.simple.yml logs -f web
```

## 🔍 Troubleshooting

### Erro: "password authentication failed"

**Solução:**
1. Verifique se `.env.production` existe e tem as variáveis corretas:
   ```bash
   cat .env.production | grep POSTGRES
   ```

2. Verifique se o container está usando as variáveis:
   ```bash
   docker exec stockbit_web env | grep POSTGRES
   ```

3. Verifique as variáveis do container db:
   ```bash
   docker exec stockbit_db env | grep POSTGRES
   ```

4. Garanta que são **exatamente iguais**!

### Erro: "Connection refused"

**Solução:**
1. Verifique se o banco está saudável:
   ```bash
   docker-compose -f docker-compose.simple.yml ps db
   ```

2. Verifique logs do banco:
   ```bash
   docker-compose -f docker-compose.simple.yml logs db
   ```

3. Aguarde o healthcheck:
   ```bash
   docker-compose -f docker-compose.simple.yml up db
   # Aguarde "database system is ready to accept connections"
   ```

### Erro: "relation does not exist"

**Solução:**
As migrações não foram executadas. Execute:
```bash
docker exec stockbit_web python manage.py migrate
```

## ✅ Checklist de Deploy

- [ ] Arquivo `.env.production` criado
- [ ] Credenciais PostgreSQL definidas em `.env.production`
- [ ] Credenciais no `.env.production` correspondem ao `docker-compose.simple.yml`
- [ ] `SECRET_KEY` alterado para uma chave aleatória
- [ ] `DEBUG=False` em produção
- [ ] `ALLOWED_HOSTS` configurado com seu domínio
- [ ] Teste de conexão executado: `./scripts/test_postgres_connection.sh`
- [ ] Containers subindo sem erros
- [ ] Migrações executadas automaticamente (via entrypoint.sh)
- [ ] Aplicação acessível

## 📝 Notas Importantes

1. **Senha Padrão**: `stockbit_password_change_me` é apenas um exemplo. **MUDE EM PRODUÇÃO!**

2. **Segurança**: Em produção, use senhas fortes e únicas:
   ```bash
   # Gerar senha aleatória
   openssl rand -base64 32
   ```

3. **Persistência**: Os dados são salvos no volume `postgres_data`. Mesmo reiniciando, os dados permanecem.

4. **Backup**: Configure backups regulares do volume PostgreSQL:
   ```bash
   docker exec stockbit_db pg_dump -U stockbit stockbit > backup.sql
   ```

