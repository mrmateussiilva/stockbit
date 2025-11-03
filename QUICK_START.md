# ⚡ Quick Start - Deploy Rápido

Guia ultra-simplificado para deploy sem Docker.

## 🎯 Versão Resumida

### 1. No Servidor

```bash
# Instalar Python e dependências
sudo apt update && sudo apt install python3 python3-pip python3-venv git nginx supervisor -y

# Clonar código
cd /opt && git clone SEU_REPOSITORIO stockbit && cd stockbit

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar .env
cp .env.production.example .env
nano .env  # Edite: SECRET_KEY, DEBUG=False, ALLOWED_HOSTS

# Migrar e criar superusuário
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### 2. Configurar Gunicorn (Supervisor)

```bash
sudo nano /etc/supervisor/conf.d/stockbit.conf
```

Cole:
```ini
[program:stockbit]
command=/opt/stockbit/venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 4 stockbit.wsgi:application
directory=/opt/stockbit
user=www-data
autostart=true
autorestart=true
```

```bash
sudo supervisorctl reread && sudo supervisorctl update && sudo supervisorctl start stockbit
```

### 3. Configurar Nginx ou Caddy

**Nginx:**
```bash
sudo nano /etc/nginx/sites-available/stockbit
```

```nginx
server {
    listen 80;
    server_name stockbit.seudominio.com;
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/stockbit /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx
```

**Ou Caddy:**
```bash
sudo nano /etc/caddy/Caddyfile
```

```caddy
stockbit.seudominio.com {
    reverse_proxy localhost:8000
}
```

```bash
sudo systemctl restart caddy
```

### 4. Configurar DNS

```
Tipo: A
Nome: stockbit
Valor: IP_DO_SERVIDOR
```

### 5. Pronto! 🎉

Acesse `http://stockbit.seudominio.com`

---

## 🔄 Atualizar Sistema

```bash
cd /opt/stockbit
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart stockbit
```

---

## 📞 Comandos Essenciais

```bash
# Ver logs
sudo tail -f /var/log/stockbit.log

# Status
sudo supervisorctl status stockbit

# Restart
sudo supervisorctl restart stockbit

# Backup SQLite
cp /opt/stockbit/db.sqlite3 /backup/db_$(date +%Y%m%d).sqlite3
```

---

**📖 Para instruções detalhadas, veja `DEPLOY.md`**
