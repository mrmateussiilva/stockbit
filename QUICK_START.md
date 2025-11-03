# ⚡ Quick Start - Deploy Rápido

Guia ultra-simplificado para quem já tem experiência com servidores.

## 🎯 Versão Resumida

### 1. No Servidor

```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh
sudo apt install docker-compose-plugin -y

# Instalar Caddy
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update && sudo apt install caddy -y

# Clonar/buscar código
cd /opt && git clone SEU_REPOSITORIO stockbit && cd stockbit

# Configurar .env.production
cp .env.production.example .env.production
nano .env.production  # Edite: SECRET_KEY, DEBUG=False, ALLOWED_HOSTS, POSTGRES_PASSWORD

# Iniciar
docker compose -f docker-compose.simple.yml build
docker compose -f docker-compose.simple.yml up -d

# Criar superusuário
docker compose -f docker-compose.simple.yml exec web python manage.py createsuperuser
```

### 2. Configurar Caddy

```bash
sudo nano /etc/caddy/Caddyfile
```

Cole (substitua o domínio):

```caddy
stockbit.seudominio.com {
    reverse_proxy localhost:8000
    handle /static/* { reverse_proxy localhost:8000 }
    handle /media/* { reverse_proxy localhost:8000 }
    tls { protocols tls1.2 tls1.3 }
}
```

```bash
sudo systemctl restart caddy
```

### 3. Configurar DNS

No seu provedor de domínio:
```
Tipo: A
Nome: stockbit
Valor: IP_DO_SERVIDOR
```

### 4. Pronto! 🎉

Acesse `https://stockbit.seudominio.com`

---

## 🔄 Atualizar Sistema

```bash
cd /opt/stockbit
git pull
docker compose -f docker-compose.simple.yml build
docker compose -f docker-compose.simple.yml up -d
```

---

## 📞 Comandos Essenciais

```bash
# Ver status
docker compose -f docker-compose.simple.yml ps

# Ver logs
docker compose -f docker-compose.simple.yml logs -f web

# Backup
docker compose -f docker-compose.simple.yml exec db pg_dump -U stockbit stockbit > backup.sql

# Restart
docker compose -f docker-compose.simple.yml restart
```

---

**📖 Para instruções detalhadas, veja `DEPLOY_SIMPLES.md`**

