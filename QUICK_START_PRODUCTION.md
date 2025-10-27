# ⚡ Quick Start - Produção

Comandos rápidos para deploy em produção com Caddy.

## 🚀 Deploy em 3 Passos

### Passo 1: Configurar
```bash
# Editar domínio
nano Caddyfile

# Configurar ambiente
cp env.production.example .env
nano .env
```

### Passo 2: Deploy
```bash
./prod.sh build

./prod.sh start
```

### Passo 3: Configurar
```bash
./prod.sh createsuperuser
./prod.sh logs
```

## 📋 Checklist Rápido

- [ ] Domínio configurado no Caddyfile
- [ ] Arquivo .env criado e configurado
- [ ] Build executado
- [ ] Serviços iniciados
- [ ] Superusuário criado
- [ ] Sistema testado

## 🎯 Comandos Mais Usados

| Comando | Descrição |
|---------|-----------|
| `./prod.sh start` | Iniciar serviços |
| `./prod.sh stop` | Parar serviços |
| `./prod.sh logs` | Ver logs |
| `./prod.sh ps` | Ver status |
| `./prod.sh backup` | Backup do banco |
| `./prod.sh restart` | Reiniciar |
| `./prod.sh update` | Atualizar sistema |

## 🔗 URLs

Após o deploy:
- Frontend: https://seudominio.com
- API: https://seudominio.com/api
- Admin: https://seudominio.com/api/admin

## 🆘 Problemas?

```bash
# Ver logs
./prod.sh logs

# Status
./prod.sh ps

# Reiniciar
./prod.sh restart
```

---

**Documentação completa:** `DEPLOY_CADDY.md`

