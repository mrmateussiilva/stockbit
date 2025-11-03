#!/bin/bash

# ============================================
# Script de Teste de Conexão PostgreSQL
# ============================================
# Testa a conexão do container web com o banco PostgreSQL

set -e

echo "============================================"
echo "Testando Conexão PostgreSQL"
echo "============================================"
echo ""

# Carrega variáveis do .env.production se existir
if [ -f .env.production ]; then
    echo "📄 Carregando variáveis de .env.production..."
    export $(grep -v '^#' .env.production | xargs)
fi

# Valores padrão
POSTGRES_DB=${POSTGRES_DB:-stockbit}
POSTGRES_USER=${POSTGRES_USER:-stockbit}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD:-stockbit_password_change_me}
POSTGRES_HOST=${POSTGRES_HOST:-db}
POSTGRES_PORT=${POSTGRES_PORT:-5432}

echo "Configuração:"
echo "  Host: $POSTGRES_HOST"
echo "  Port: $POSTGRES_PORT"
echo "  Database: $POSTGRES_DB"
echo "  User: $POSTGRES_USER"
echo ""

# Verifica se os containers estão rodando
echo "1️⃣ Verificando containers..."
if ! docker ps | grep -q stockbit_db; then
    echo "❌ Container stockbit_db não está rodando!"
    echo "   Execute: docker-compose -f docker-compose.simple.yml up -d"
    exit 1
fi

if ! docker ps | grep -q stockbit_web; then
    echo "⚠️  Container stockbit_web não está rodando (não é crítico para este teste)"
fi

echo "✅ Containers encontrados"
echo ""

# Testa conexão do host
echo "2️⃣ Testando conexão do HOST..."
if command -v psql &> /dev/null; then
    if PGPASSWORD="$POSTGRES_PASSWORD" psql -h localhost -p 5432 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT 1;" &> /dev/null; then
        echo "✅ Conexão do host OK"
    else
        echo "⚠️  Não foi possível conectar do host (normal se porta não estiver exposta)"
    fi
else
    echo "⚠️  psql não instalado no host (não é crítico)"
fi
echo ""

# Testa conexão do container web
echo "3️⃣ Testando conexão do CONTAINER WEB..."
if docker ps | grep -q stockbit_web; then
    echo "Executando teste de conexão no container..."
    docker exec stockbit_web python -c "
import os
import psycopg2
from django.conf import settings

# Configura manualmente (simula settings.py)
db_config = {
    'host': os.getenv('POSTGRES_HOST', 'db'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'stockbit'),
    'user': os.getenv('POSTGRES_USER', 'stockbit'),
    'password': os.getenv('POSTGRES_PASSWORD', 'stockbit_password_change_me'),
}

try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('SELECT version();')
    version = cursor.fetchone()[0]
    print('✅ Conexão estabelecida com sucesso!')
    print(f'   PostgreSQL: {version.split()[0]} {version.split()[1]}')
    cursor.close()
    conn.close()
except psycopg2.Error as e:
    print(f'❌ ERRO na conexão: {e}')
    exit(1)
" || {
        echo "❌ Falha no teste de conexão do container web"
        exit 1
    }
else
    echo "⚠️  Container stockbit_web não está rodando"
    echo "   Testando diretamente no container db..."
    docker exec stockbit_db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT version();" || {
        echo "❌ Erro ao conectar no banco"
        exit 1
    }
    echo "✅ Conexão direta ao banco OK"
fi
echo ""

# Testa via Django
echo "4️⃣ Testando via Django (settings.py)..."
if docker ps | grep -q stockbit_web; then
    docker exec stockbit_web python manage.py check --database default 2>&1 | grep -q "System check identified" && {
        echo "✅ Django consegue conectar ao banco"
    } || {
        echo "⚠️  Django pode ter problemas de conexão (verifique logs)"
    }
else
    echo "⚠️  Container web não está rodando"
fi
echo ""

echo "============================================"
echo "✅ Teste concluído!"
echo "============================================"

