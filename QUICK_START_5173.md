# Setup Rápido - Frontend na Porta 5173

## Configuração

O frontend agora roda internamente na **porta 5173** usando o Vite dev server.

## Estrutura

```
Caddy (seu Caddyfile)
    ↓
Frontend:5173 (Vite dev server)
    ↓
Backend:8000 (Django/Gunicorn)
```

## Seu Caddyfile

Você precisa configurar o proxy reverso para `frontend:5173`:

```caddy
stockbit.finderbit.com.br {
    # API
    handle /api/* {
        reverse_proxy backend:8000
    }

    # Frontend (porta 5173)
    handle {
        reverse_proxy frontend:5173
    }
}
```

Veja o exemplo completo em: `Caddyfile.example`

## Comandos

### Subir os containers
```bash
docker-compose -f docker-compose.prod-caddy-sqlite.yml up -d --build
```

### Ver logs
```bash
docker-compose -f docker-compose.prod-caddy-sqlite.yml logs -f frontend
```

### Parar
```bash
docker-compose -f docker-compose.prod-caddy-sqlite.yml down
```

## Diferenças do modo Dev vs Prod

### Modo DEV (5173) - Atual
- ✅ Hot reload automático
- ✅ Recompilação rápida
- ✅ Melhor para desenvolvimento
- ❌ Não é otimizado para produção

### Modo PROD (build + nginx)
- ✅ Assets otimizados e minificados
- ✅ Melhor performance
- ✅ Pronto para produção
- ❌ Sem hot reload

## Credenciais

- **Username:** finderbit
- **Password:** finderbit3010

## Testar

```bash
# Testar se o frontend está rodando
curl http://localhost:5173

# Testar através do Caddy (sua porta configurada)
curl https://stockbit.finderbit.com.br
```

