# Configuração do Nginx como Proxy Reverso

O Caddy está configurado para rodar nas portas **8080** (HTTP) e **8443** (HTTPS). Você precisa configurar o Nginx na porta 80/443 para fazer proxy reverso.

## Passo a Passo

### 1. Subir os containers Docker

```bash
docker-compose -f docker-compose.prod-c-capy-sqlite.yml up -d --build
```

### 2. Configurar o Nginx

Crie ou edite o arquivo de configuração do Nginx:

```bash
sudo nano /etc/nginx/sites-available/stockbit
```

Cole o seguinte conteúdo:

```nginx
# HTTP - redireciona para HTTPS
server {
    listen 80;
    server_name stockbit.finderbit.com.br;
    
    return 301 https://$server_name$request_uri;
}

# HTTPS - Proxy reverso para o Caddy
server {
    listen 443 ssl http2;
    server_name stockbit.finderbit.com.br;
    
    # Certificados SSL (ajuste o caminho)
    ssl_certificate /etc/letsencrypt/live/stockbit.finderbit.com.br/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/stockbit.finderbit.com.br/privkey.pem;
    
    # Timeouts
    proxy_connect_timeout 120s;
    proxy_send_timeout 120s;
    proxy_read_timeout 120s;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_buffering off;
    }
}
```

### 3. Habilitar o site

```bash
# Criar link simbólico
sudo ln -s /etc/nginx/sites-available/stockbit /etc/nginx/sites-enabled/

# Testar configuração
sudo nginx -t

# Recarregar nginx
sudo systemctl reload nginx
```

### 4. Gerar certificado SSL (se necessário)

```bash
sudo certbot --nginx -d stockbit.finderbit.com.br
```

## Verificar

```bash
# Ver logs do Caddy
docker-compose -f docker-compose.prod-caddy-sqlite.yml logs caddy

# Ver logs do nginx
sudo tail -f /var/log/nginx/stockbit_access.log
```

## Estrutura

```
Internet (Porta 443)
    ↓
Nginx (localhost:443)
    ↓ (proxy reverso)
Caddy (localhost:8080)
    ↓
Frontend + Backend (Docker)
```

## Acesso

- **URL:** https://stockbit.finderbit.com.br
- **Login:** finderbit
- **Senha:** finderbit3010

## Troubleshooting

### Caddy não está acessível na 8080
```bash
# Ver se o container está rodando
docker-compose -f docker-compose.prod-caddy-sqlite.yml ps

# Ver logs
docker-compose -f docker-compose.prod-caddy-sqlite.yml logs caddy
```

### Testar conexão direta com Caddy
```bash
# Deve retornar o HTML
curl http://localhost:8080
```

### Testar através do Nginx
```bash
# Deve retornar o HTML também
curl http://stockbit.finderbit.com.br
```

