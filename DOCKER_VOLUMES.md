# 📦 Volumes Docker - Persistência de Dados

## ✅ SIM! Os dados são persistidos!

Os dados **permanecem salvos** mesmo após parar e reiniciar os containers.

## 🔍 Como Funciona

### Volumes Configurados

O docker-compose cria 3 volumes persistentes:

1. **`postgres_data`** - Banco de dados PostgreSQL
   - Localização: `/var/lib/postgresql/data`
   - **Contém TODO o banco de dados** (produtos, categorias, fornecedores, movimentações)

2. **`static_volume`** - Arquivos estáticos (CSS, JS, imagens compiladas)
   - Localização: `/app/staticfiles`
   - Arquivos gerados pelo `collectstatic`

3. **`media_volume`** - Arquivos de upload (XMLs, documentos)
   - Localização: `/app/media`
   - Arquivos enviados pelos usuários

## 🔄 O Que Acontece ao Parar/Reiniciar

### ✅ Dados PERMANECEM (Comportamento Normal)

```bash
# Parar os containers
docker-compose -f docker-compose.simple.yml down

# Reiniciar
docker-compose -f docker-compose.simple.yml up -d
```

**Resultado:** Todos os dados ainda estão lá! ✅

### ⚠️ Dados são APAGADOS (Apenas com -v)

```bash
# CUIDADO: Isto APAGA TODOS OS DADOS!
docker-compose -f docker-compose.simple.yml down -v
```

**Resultado:** TODOS os volumes são deletados! ⚠️

## 📍 Localização dos Volumes

Os volumes ficam armazenados em:

```bash
/var/lib/docker/volumes/stockbit_postgres_data/
/var/lib/docker/volumes/stockbit_static_volume/
/var/lib/docker/volumes/stockbit_media_volume/
```

### Ver Volumes

```bash
# Listar todos os volumes
docker volume ls

# Ver detalhes de um volume específico
docker volume inspect stockbit_postgres_data

# Ver o tamanho do banco de dados
docker volume inspect stockbit_postgres_data | grep Mountpoint
sudo du -sh $(docker volume inspect stockbit_postgres_data --format '{{ .Mountpoint }}')
```

## 💾 Backup dos Dados

### Backup Manual

```bash
# Backup do banco de dados
docker-compose -f docker-compose.simple.yml exec db pg_dump -U stockbit stockbit > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup de um volume inteiro
docker run --rm -v stockbit_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz /data
```

### Backup Automatizado (Cron)

```bash
# Crie o script de backup
cat > /usr/local/bin/backup-stockbit.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/stockbit"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup do banco
docker-compose -f /path/to/stockbit/docker-compose.simple.yml exec -T db pg_dump -U stockbit stockbit > $BACKUP_DIR/db_$DATE.sql

# Backup dos volumes
docker run --rm -v stockbit_postgres_data:/data -v stockbit_media_volume:/media -v $BACKUP_DIR:/backup alpine tar czf /backup/volumes_$DATE.tar.gz /data /media

# Manter apenas os últimos 7 backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
EOF

chmod +x /usr/local/bin/backup-stockbit.sh

# Configure cron (backup diário às 3h da manhã)
echo "0 3 * * * /usr/local/bin/backup-stockbit.sh" | crontab -
```

## 🔄 Migrar Dados

### Entre Servidores

1. **No servidor original:**

```bash
# Backup
docker-compose -f docker-compose.simple.yml exec db pg_dump -U stockbit stockbit > backup.sql

# Copiar arquivos de media
docker cp stockbit_web:/app/media ./media_backup
```

2. **No novo servidor:**

```bash
# Subir containers vazios
docker-compose -f docker-compose.simple.yml up -d

# Aguardar banco ficar pronto
sleep 10

# Restaurar banco
docker-compose -f docker-compose.simple.yml exec -T db psql -U stockbit stockbit < backup.sql

# Restaurar media
docker cp ./media_backup/. stockbit_web:/app/media
```

## 🔍 Verificar Persistência

### Teste Prático

```bash
# 1. Crie alguns dados no sistema
#    - Cadastre produtos, categorias, etc.

# 2. Parar containers
docker-compose -f docker-compose.simple.yml down

# 3. Verificar que volumes ainda existem
docker volume ls | grep stockbit
# Deve mostrar: stockbit_postgres_data, stockbit_static_volume, stockbit_media_volume

# 4. Reiniciar
docker-compose -f docker-compose.simple.yml up -d

# 5. Acessar o sistema
# Todos os dados estão lá! ✅
```

### Inspecionar Banco

```bash
# Conectar ao PostgreSQL
docker-compose -f docker-compose.simple.yml exec db psql -U stockbit stockbit

# Dentro do PostgreSQL:
SELECT COUNT(*) FROM estoque_product;
SELECT COUNT(*) FROM estoque_category;
SELECT COUNT(*) FROM estoque_stockmovement;

# Sair
\q
```

## 🚨 Cuidados Importantes

### ⚠️ NÃO USE `-v` em Produção

```bash
# ❌ ERRO: Apaga todos os dados!
docker-compose -f docker-compose.simple.yml down -v
```

### ⚠️ Backup ANTES de Atualizar

```bash
# 1. Backup
docker-compose -f docker-compose.simple.yml exec db pg_dump -U stockbit stockbit > backup_pre_update.sql

# 2. Atualizar
git pull
docker-compose -f docker-compose.simple.yml build --no-cache
docker-compose -f docker-compose.simple.yml up -d

# 3. Se der problema, restaure
docker-compose -f docker-compose.simple.yml exec -T db psql -U stockbit stockbit < backup_pre_update.sql
```

## 📊 Monitoramento de Espaço

```bash
# Ver uso de disco dos volumes
docker system df -v

# Ver tamanho específico de um volume
sudo du -sh $(docker volume inspect stockbit_postgres_data --format '{{ .Mountpoint }}')

# Limpar volumes não utilizados (CUIDADO!)
docker volume prune
```

## 🔗 Links Úteis

- [Docker Volumes Documentation](https://docs.docker.com/storage/volumes/)
- [PostgreSQL Backup and Restore](https://www.postgresql.org/docs/current/backup.html)

## ✅ Checklist

- [ ] Entendi que dados são persistidos
- [ ] Configurei backup automático
- [ ] Sei onde estão os volumes
- [ ] Tenho plano de restauração
- [ ] Não uso `-v` acidentalmente

