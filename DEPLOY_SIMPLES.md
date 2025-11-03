# 🚀 Guia de Deploy Simplificado - StockBit

Guia passo a passo simples para fazer deploy do StockBit em produção.

## 📋 Pré-requisitos

1. **Servidor Linux** (Ubuntu 22.04 ou similar)
2. **Acesso root ou sudo**
3. **Domínio configurado** (ex: `stockbit.seudominio.com`)
4. **Docker e Docker Compose instalados**

---

## 🔧 Passo 1: Preparar o Servidor

### 1.1 Instalar Docker

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
newgrp docker  # Ou faça logout/login

# Instalar Docker Compose
sudo apt install docker-compose-plugin -y

# Verificar instalação
docker --version
docker compose version
```

### 1.2 Instalar Caddy (Reverse Proxy)

```bash
# Adicionar repositório do Caddy
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update

# Instalar Caddy
sudo apt install caddy -y

# Verificar instalação
caddy version
```

---

## 📦 Passo 2: Preparar o Código

### 2.1 No Seu Computador Local

```bash
# 1. Certifique-se de que tudo está commitado
git status

# 2. Crie um arquivo .env.production com as variáveis necessárias
cp .env.production.example .env.production
nano .env.production  # Edite com suas configurações
```

### 2.2 Configurar .env.production

Edite o arquivo `.env.production`:

```bash
# SECRET_KEY - GERE UMA CHAVE ÚNICA!
SECRET_KEY=sua_chave_secreta_aqui_use_um_comando_para_gerar

# DEBUG - SEMPRE False em produção!
DEBUG=False

# ALLOWED_HOSTS - Seu domínio
ALLOWED_HOSTS=stockbit.seudominio.com,www.stockbit.seudominio.com

# PostgreSQL (mesmas credenciais do docker-compose)
POSTGRES_DB=stockbit
POSTGRES_USER=stockbit
POSTGRES_PASSWORD=SENHA_SEGURA_AQUI_TROQUE_ISSO

# Host e porta (não mude, a menos que use banco externo)
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Security (mude para True se usar HTTPS válido)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

**Gerar SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🚢 Passo 3: Enviar Código para o Servidor

### 3.1 Via Git (Recomendado)

```bash
# No servidor, clonar o repositório
cd /opt  # ou outro diretório de sua preferência
git clone https://github.com/seu-usuario/stockbit.git
cd stockbit
```

### 3.2 Via SCP (Alternativa)

```bash
# No seu computador local
scp -r /caminho/para/stockbit usuario@servidor:/opt/
```

### 3.3 Criar .env.production no Servidor

```bash
# No servidor
cd /opt/stockbit
nano .env.production  # Cole o conteúdo do .env.production que você preparou
```

---

## 🐳 Passo 4: Configurar Docker

### 4.1 Ajustar docker-compose.simple.yml (se necessário)

O arquivo já está pronto, mas você pode ajustar as credenciais:

```bash
# No servidor
cd /opt/stockbit
nano docker-compose.simple.yml
```

Verifique se as variáveis de ambiente estão corretas:
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`

**⚠️ IMPORTANTE:** As credenciais no `docker-compose.simple.yml` devem ser **exatamente iguais** às do `.env.production`!

### 4.2 Construir e Iniciar Containers

```bash
# Construir imagens
docker compose -f docker-compose.simple.yml build

# Iniciar containers
docker compose -f docker-compose.simple.yml up -d

# Verificar se estão rodando
docker compose -f docker-compose.simple.yml ps

# Ver logs (se houver erros)
docker compose -f docker-compose.simple.yml logs -f
```

**O que acontece:**
- Cria containers para PostgreSQL e Django
- Executa migrações automaticamente
- Coleta arquivos estáticos
- Inicia o servidor Gunicorn na porta 8000

---

## 🌐 Passo 5: Configurar Caddy (Reverse Proxy)

### 5.1 Criar Caddyfile

```bash
# No servidor
sudo nano /etc/caddy/Caddyfile
```

Cole o seguinte conteúdo (substitua pelo seu domínio):

```caddy
stockbit.seudominio.com {
    # Proxy para o container Docker
    reverse_proxy localhost:8000 {
        header_up Connection "Keep-Alive"
        transport http {
            dial_timeout 10s
            response_header_timeout 30s
            idle_timeout 90s
        }
    }
    
    # Servir arquivos estáticos
    handle /static/* {
        reverse_proxy localhost:8000
    }
    
    # Servir arquivos de media (upload)
    handle /media/* {
        reverse_proxy localhost:8000
    }
    
    # Headers de segurança
    header {
        -Server
        X-Content-Type-Options "nosniff"
        X-Frame-Options "SAMEORIGIN"
        X-XSS-Protection "1; mode=block"
        Referrer-Policy "no-referrer-when-downgrade"
    }
    
    # Compressão
    encode gzip zstd
    
    # Logs
    log {
        output file /var/log/caddy/stockbit.log {
            roll_size 100mb
            roll_keep 10
        }
    }
    
    # TLS automático (Let's Encrypt)
    tls {
        protocols tls1.2 tls1.3
    }
}
```

### 5.2 Configurar DNS

No seu provedor de domínio, adicione um registro A apontando para o IP do servidor:

```
Tipo: A
Nome: stockbit (ou @)
Valor: IP_DO_SEU_SERVIDOR
TTL: 3600
```

**Como descobrir o IP do servidor:**
```bash
curl ifconfig.me
# ou
hostname -I
```

### 5.3 Iniciar Caddy

```bash
# Testar configuração
sudo caddy validate --config /etc/caddy/Caddyfile

# Se estiver tudo ok, iniciar/reiniciar Caddy
sudo systemctl restart caddy

# Verificar status
sudo systemctl status caddy

# Ver logs
sudo journalctl -u caddy -f
```

### 5.4 Verificar Certificado SSL

O Caddy obtém automaticamente o certificado SSL do Let's Encrypt na primeira vez que acessa o domínio. Aguarde alguns minutos e verifique:

```bash
# Ver logs do Caddy
sudo journalctl -u caddy -f
```

---

## 👤 Passo 6: Criar Superusuário

```bash
# Acessar o container
docker compose -f docker-compose.simple.yml exec web bash

# Dentro do container, criar superusuário
python manage.py createsuperuser

# Sair do container
exit
```

---

## ✅ Passo 7: Verificar se Está Funcionando

### 7.1 Testar Acesso

1. Abra o navegador e acesse: `https://stockbit.seudominio.com`
2. Você deve ver a página de login
3. Faça login com o superusuário criado

### 7.2 Verificar Logs

```bash
# Logs dos containers
docker compose -f docker-compose.simple.yml logs web
docker compose -f docker-compose.simple.yml logs db

# Logs do Caddy
sudo journalctl -u caddy -f
```

### 7.3 Verificar Status dos Containers

```bash
docker compose -f docker-compose.simple.yml ps
```

Todos devem estar com status "Up".

---

## 🔄 Passo 8: Atualizar o Sistema (Futuro)

Quando fizer alterações no código:

```bash
# No servidor
cd /opt/stockbit

# Atualizar código
git pull  # ou faça upload dos arquivos novos

# Reconstruir e reiniciar
docker compose -f docker-compose.simple.yml build
docker compose -f docker-compose.simple.yml up -d

# Executar migrações (se houver novas)
docker compose -f docker-compose.simple.yml exec web python manage.py migrate

# Recoletar arquivos estáticos (se houver mudanças)
docker compose -f docker-compose.simple.yml exec web python manage.py collectstatic --noinput
```

---

## 🔒 Passo 9: Configurações de Segurança (Opcional)

### 9.1 Ativar HTTPS e Segurança

Edite `.env.production`:

```bash
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

Depois reinicie:
```bash
docker compose -f docker-compose.simple.yml restart web
```

### 9.2 Firewall

```bash
# Instalar UFW (se não tiver)
sudo apt install ufw -y

# Permitir SSH
sudo ufw allow 22/tcp

# Permitir HTTP e HTTPS (Caddy)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Ativar firewall
sudo ufw enable

# Verificar status
sudo ufw status
```

---

## 🐛 Troubleshooting (Solução de Problemas)

### Problema: Containers não iniciam

```bash
# Ver logs detalhados
docker compose -f docker-compose.simple.yml logs

# Verificar se a porta 8000 está livre
sudo netstat -tulpn | grep 8000

# Verificar espaço em disco
df -h
```

### Problema: Erro de conexão com banco

```bash
# Verificar se o banco está saudável
docker compose -f docker-compose.simple.yml ps db

# Verificar logs do banco
docker compose -f docker-compose.simple.yml logs db

# Conectar manualmente ao banco
docker compose -f docker-compose.simple.yml exec db psql -U stockbit stockbit
```

### Problema: Caddy não obtém certificado SSL

```bash
# Ver logs do Caddy
sudo journalctl -u caddy -f

# Verificar se o DNS está propagado
nslookup stockbit.seudominio.com

# Verificar se as portas 80 e 443 estão abertas
sudo ufw status
```

### Problema: Erro 502 Bad Gateway

Isso significa que o Caddy não consegue se conectar ao Django:

```bash
# Verificar se o container web está rodando
docker compose -f docker-compose.simple.yml ps web

# Verificar logs do container web
docker compose -f docker-compose.simple.yml logs web

# Testar se a porta 8000 responde localmente
curl http://localhost:8000
```

### Problema: Erro de migrações

```bash
# Executar migrações manualmente
docker compose -f docker-compose.simple.yml exec web python manage.py migrate
```

---

## 📊 Checklist Final

- [ ] Docker e Docker Compose instalados
- [ ] Caddy instalado e rodando
- [ ] Arquivo `.env.production` configurado
- [ ] `docker-compose.simple.yml` com credenciais corretas
- [ ] Containers rodando (`docker compose ps`)
- [ ] Caddyfile configurado corretamente
- [ ] DNS configurado (registro A)
- [ ] Certificado SSL obtido (verificar em `https://`)
- [ ] Superusuário criado
- [ ] Acesso ao sistema funcionando
- [ ] Login funcionando
- [ ] Firewall configurado (opcional)

---

## 📞 Comandos Úteis

```bash
# Parar containers
docker compose -f docker-compose.simple.yml down

# Iniciar containers
docker compose -f docker-compose.simple.yml up -d

# Reiniciar containers
docker compose -f docker-compose.simple.yml restart

# Ver logs em tempo real
docker compose -f docker-compose.simple.yml logs -f

# Acessar shell do container web
docker compose -f docker-compose.simple.yml exec web bash

# Backup do banco de dados
docker compose -f docker-compose.simple.yml exec db pg_dump -U stockbit stockbit > backup_$(date +%Y%m%d).sql

# Restaurar backup
docker compose -f docker-compose.simple.yml exec -T db psql -U stockbit stockbit < backup_20240101.sql

# Reiniciar Caddy
sudo systemctl restart caddy

# Ver status do Caddy
sudo systemctl status caddy
```

---

## 📚 Próximos Passos

1. **Backup Automatizado**: Configure backups regulares do banco de dados
2. **Monitoramento**: Configure alertas e monitoramento
3. **Logs**: Configure rotação de logs
4. **Performance**: Ajuste conforme necessidade

---

**🎉 Pronto! Seu sistema StockBit está em produção!**

