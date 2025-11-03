# 🔧 Solução de Problemas de Permissão no Docker

## Problema

Erro ao executar `collectstatic`:
```
PermissionError: [Errno 13] Permission denied: '/app/staticfiles/admin'
```

## Causa

Os volumes Docker são criados pelo root quando montados pela primeira vez, e o container roda como usuário `stockbit` (UID 1000).

## ✅ Soluções

### Solução 1: Ajustar Permissões Manualmente (Recomendado)

**Após criar os volumes pela primeira vez:**

```bash
# Parar containers
docker compose -f docker-compose.simple.yml down

# Ajustar permissões dos volumes
sudo chown -R 1000:1000 $(docker volume inspect stockbit_static_volume --format '{{ .Mountpoint }}')
sudo chown -R 1000:1000 $(docker volume inspect stockbit_media_volume --format '{{ .Mountpoint }}')

# Reiniciar containers
docker compose -f docker-compose.simple.yml up -d
```

### Solução 2: Usar Script de Inicialização

```bash
# Executar script de correção
chmod +x fix-permissions.sh
./fix-permissions.sh

# Reiniciar containers
docker compose -f docker-compose.simple.yml restart web
```

### Solução 3: Deletar Volumes e Recriar (Útil na Primeira Vez)

```bash
# ⚠️ ATENÇÃO: Isso apaga os dados dos volumes!
docker compose -f docker-compose.simple.yml down -v

# Ajustar permissões ANTES de criar os volumes
# (O Docker cria com permissões do root, mas podemos ajustar depois)

# Recriar tudo
docker compose -f docker-compose.simple.yml up -d

# Depois ajustar permissões
sudo chown -R 1000:1000 $(docker volume inspect stockbit_static_volume --format '{{ .Mountpoint }}')
sudo chown -R 1000:1000 $(docker volume inspect stockbit_media_volume --format '{{ .Mountpoint }}')

# Reiniciar container web
docker compose -f docker-compose.simple.yml restart web
```

### Solução 4: Executar collectstatic Manualmente Como Root (Temporário)

```bash
# Executar collectstatic como root dentro do container
docker compose -f docker-compose.simple.yml exec --user root web python manage.py collectstatic --noinput

# Ajustar permissões depois
docker compose -f docker-compose.simple.yml exec --user root web chown -R stockbit:stockbit /app/staticfiles
```

## 🔍 Verificar Permissões

```bash
# Ver quem é o dono dos volumes
docker compose -f docker-compose.simple.yml exec --user root web ls -la /app/staticfiles

# Ver UID do usuário stockbit
docker compose -f docker-compose.simple.yml exec web id
# Deve mostrar: uid=1000(stockbit) gid=1000(stockbit)
```

## 🚀 Solução Definitiva (Para Novos Deploys)

Para evitar esse problema no futuro, ajuste as permissões logo após criar os volumes:

```bash
# 1. Criar containers
docker compose -f docker-compose.simple.yml up -d

# 2. Aguardar volumes serem criados
sleep 5

# 3. Ajustar permissões
sudo chown -R 1000:1000 $(docker volume inspect stockbit_static_volume --format '{{ .Mountpoint }}')
sudo chown -R 1000:1000 $(docker volume inspect stockbit_media_volume --format '{{ .Mountpoint }}')

# 4. Reiniciar container web para coletar estáticos
docker compose -f docker-compose.simple.yml restart web
```

## 📝 Nota Importante

O erro de permissão no `collectstatic` não impede a aplicação de funcionar. Os arquivos estáticos são coletados automaticamente quando necessário, mas pode haver problemas ao servir arquivos do admin do Django.

Se o erro persistir, você pode:
1. Ignorar o erro (a aplicação funciona sem os estáticos coletados)
2. Executar `collectstatic` manualmente depois
3. Ajustar as permissões conforme as soluções acima

