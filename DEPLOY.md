# 🚀 Guia de Deploy - StockBit

Guia simples para fazer deploy do StockBit em produção.

## 📋 Pré-requisitos

1. **Servidor Linux** (Ubuntu 22.04 ou similar)
2. **Python 3.12+** instalado
3. **Acesso SSH** ao servidor

---

## 🔧 Passo 1: Preparar o Servidor

### 1.1 Instalar Python e Dependências

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e pip
sudo apt install python3 python3-pip python3-venv -y

# Instalar outras dependências
sudo apt install git nginx supervisor -y
```

### 1.2 Instalar Caddy (Reverse Proxy - Opcional)

```bash
# Adicionar repositório do Caddy
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy -y
```

---

## 📦 Passo 2: Preparar o Código

### 2.1 Clonar o Repositório

```bash
# Criar diretório para aplicações
sudo mkdir -p /opt
cd /opt

# Clonar repositório
git clone SEU_REPOSITORIO stockbit
cd stockbit
```

### 2.2 Criar Ambiente Virtual

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.3 Configurar Variáveis de Ambiente

```bash
# Criar arquivo .env
cp .env.production.example .env
nano .env
```

Configure pelo menos:
```bash
SECRET_KEY=sua_chave_secreta_gerada_aqui
DEBUG=False
ALLOWED_HOSTS=stockbit.seudominio.com,www.stockbit.seudominio.com
```

**Gerar SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🗄️ Passo 3: Configurar Banco de Dados

```bash
# Executar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic --noinput
```

---

## 🌐 Passo 4: Configurar Servidor Web

### Opção A: Usando Caddy (Recomendado - SSL Automático)

```bash
# Criar Caddyfile
sudo nano /etc/caddy/Caddyfile
```

Adicione:
```caddy
stockbit.seudominio.com {
    reverse_proxy localhost:8000
    handle /static/* { reverse_proxy localhost:8000 }
    handle /media/* { reverse_proxy localhost:8000 }
    tls { protocols tls1.2 tls1.3 }
}
```

```bash
# Reiniciar Caddy
sudo systemctl restart caddy
```

### Opção B: Usando Nginx

```bash
# Criar configuração do Nginx
sudo nano /etc/nginx/sites-available/stockbit
```

Adicione:
```nginx
server {
    listen 80;
    server_name stockbit.seudominio.com;

    location /static/ {
        alias /opt/stockbit/staticfiles/;
    }

    location /media/ {
        alias /opt/stockbit/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/stockbit /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🚀 Passo 5: Configurar Gerenciador de Processos

### Usando Supervisor

```bash
# Criar configuração do Supervisor
sudo nano /etc/supervisor/conf.d/stockbit.conf
```

Adicione:
```ini
[program:stockbit]
command=/opt/stockbit/venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 4 --timeout 120 stockbit.wsgi:application
directory=/opt/stockbit
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/stockbit.log
environment=DJANGO_SETTINGS_MODULE="stockbit.settings"
```

```bash
# Recarregar Supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start stockbit
```

### Ou usando systemd

```bash
# Criar serviço systemd
sudo nano /etc/systemd/system/stockbit.service
```

Adicione:
```ini
[Unit]
Description=StockBit Django Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/stockbit
Environment="PATH=/opt/stockbit/venv/bin"
ExecStart=/opt/stockbit/venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 4 stockbit.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Iniciar serviço
sudo systemctl daemon-reload
sudo systemctl enable stockbit
sudo systemctl start stockbit
```

---

## 🔒 Passo 6: Configurar DNS

No seu provedor de domínio, adicione um registro A:

```
Tipo: A
Nome: stockbit (ou @)
Valor: IP_DO_SEU_SERVIDOR
TTL: 3600
```

---

## ✅ Passo 7: Verificar

1. Acesse `http://stockbit.seudominio.com` (ou `https://` se usar Caddy)
2. Verifique se a página de login aparece
3. Faça login com o superusuário criado

---

## 🔄 Atualizar Sistema

```bash
cd /opt/stockbit
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo supervisorctl restart stockbit  # ou systemctl restart stockbit
```

---

## 📊 Comandos Úteis

```bash
# Ver logs
sudo tail -f /var/log/stockbit.log

# Verificar status
sudo supervisorctl status stockbit  # ou systemctl status stockbit

# Reiniciar aplicação
sudo supervisorctl restart stockbit  # ou systemctl restart stockbit

# Backup do banco SQLite
cp /opt/stockbit/db.sqlite3 /backup/db_$(date +%Y%m%d).sqlite3
```

---

## 🐛 Troubleshooting

### Erro 502 Bad Gateway
- Verifique se o Gunicorn está rodando: `sudo supervisorctl status stockbit`
- Verifique logs: `sudo tail -f /var/log/stockbit.log`

### Erro de permissões
```bash
sudo chown -R www-data:www-data /opt/stockbit
sudo chmod -R 755 /opt/stockbit
```

### Banco de dados bloqueado
SQLite pode ter problemas com concorrência. Se isso acontecer, considere usar PostgreSQL para produção.

---

**🎉 Pronto! Seu sistema StockBit está em produção!**

