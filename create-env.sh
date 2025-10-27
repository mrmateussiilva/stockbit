#!/bin/bash

# Script para criar o arquivo .env para produção com SQLite
# Uso: bash create-env.sh

echo "Criando arquivo .env para produção com SQLite..."

# Gerar SECRET_KEY aleatório
SECRET_KEY=$(openssl rand -base64 64 | tr -d '\n')

cat > .env << EOF
# Configurações de Ambiente para Produção - Stockbit (SQLite)
# Gerado automaticamente

# Django Settings
SECRET_KEY=${SECRET_KEY}
DEBUG=False
ALLOWED_HOSTS=stockbit.finderbit.com.br,finderbit.com.br,localhost,127.0.0.1,caddy

# SQLite (não precisa de configuração - usa padrão do Django)
# O banco será criado automaticamente em /app/db.sqlite3

# CORS Settings
CORS_ALLOWED_ORIGINS=https://stockbit.finderbit.com.br,https://finderbit.com.br

# API Settings
VITE_API_URL=https://stockbit.finderbit.com.br/api

# Security Settings
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE=True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Logging
LOG_LEVEL=INFO

# Timezone
TIME_ZONE=America/Sao_Paulo
EOF

echo "✅ Arquivo .env criado com sucesso (SQLite)!"
echo ""
echo "SECRET_KEY gerada automaticamente."
echo "O banco SQLite será criado automaticamente pelo Django."