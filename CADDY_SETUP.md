# Setup do Caddy - Stockbit

## Estrutura de Portas

O Caddy está configurado para rodar com as seguintes portas:

- **Porta 8080** (HTTP) - Para desenvolvimento local
- **Porta 8443** (HTTPS) - Para produção com SSL
- **Porta 80/443** - Portas internas do container

## Como Funciona

```
Internet (Porta 443)
    ↓
Caddy (Porta 8080/8443)
    ↓
Frontend Container (Porta 80 interna)
```

## Acesso

### Produção (com domínio)
- **URL:** https://stockbit.finderbit.com.br
- **Porta usada:** 8443 (mapeada para 443 interna)
- **SSL:** Automático via Let's Encrypt

### Desenvolvimento Local
- **URL:** http://localhost:8080
- **API:** http://localhost:8080/api
- **SSL:** Não necessário

## Comandos

### Subir os containers
```bash
docker-compose -f docker-compose.prod-caddy-sqlite.yml up -d --build
```

### Ver logs
```bash
# Todos os logs
docker-compose -f docker-compose.prod-caddy-sqlite.yml logs -f

# Só Caddy
docker-compose -f docker-compose.prod-caddy-sqlite.yml logs -f caddy

# Só Backend
docker-compose -f docker-compose.prod-caddy-sqlite.yml logs -f backend

# Só Frontend
docker-compose -f docker-compose.prod-caddy-sqlite.yml logs -f frontend
```

### Parar tudo
```bash
docker-compose -f docker-compose.prod-caddy-sqlite.yml down
```

## Credenciais

- **Username:** finderbit
- **Password:** finderbit3010
- **Email:** admin@finderbit.com.br

## Verificação

### Testar se o Caddy está rodando
```bash
# Deve retornar HTML da aplicação
curl http://localhost:8080

# Testar API
curl http://localhost:8080/api/products/categories/
```

### Ver containers rodando
```bash
docker-compose -f docker-compose.prod-caddy-sqlite.yml ps
```

### Entrar no container do backend
```bash
docker-compose -f docker-compose.prod-caddy-sqlite.yml exec backend bash
```

## Troubleshooting

### Caddy não inicia
```bash
# Ver logs de erro
docker-compose -f docker-compose.prod-caddy-sqlite.yml logs caddy

# Verificar sintaxe do Caddyfile
docker-compose -f docker-compose.prod-caddy-sqlite.yml exec caddy caddy validate --config /etc/caddy/Caddyfile
```

### Frontend não carrega CSS
```bash
# Rebuild sem cache
docker-compose -f docker-compose.prod-caddy-sqlite.yml down
docker-compose -f docker-compose.prod-caddy-sqlite.yml build --no-cache frontend
docker-compose -f docker-compose.prod-caddy-sqlite.yml up -d
```

### Porta 8080 já em uso
```bash
# Ver o que está usando
sudo lsof -i :8080

# Ou mudar a porta no docker-compose.prod-caddy-sqlite.yml
# Trocar "8080:80" por outra porta, ex: "8081:80"
```

## Arquivos Importantes

- `Caddyfile` - Configuração do Caddy
- `docker-compose.prod-caddy-sqlite.yml` - Orquestração dos containers
- `.env` - Variáveis de ambiente

## Próximos Passos

1. ✅ Configurar DNS para apontar para seu servidor
2. ✅ Subir os containers
3. ✅ Acessar via domínio: https://stockbit.finderbit.com.br
4. ✅ Fazer login e alterar a senha padrão
5. ✅ Criar backup do banco SQLite periodicamente

