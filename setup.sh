#!/bin/bash

# Script de inicialização do projeto Stockbit
# Este script configura e executa o projeto completo

set -e

echo "🚀 Iniciando configuração do Stockbit..."

# Verificar se o Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Por favor, instale o Docker primeiro."
    exit 1
fi

# Verificar se o Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose não está instalado. Por favor, instale o Docker Compose primeiro."
    exit 1
fi

# Criar arquivo .env se não existir
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    cp env.example .env
    echo "✅ Arquivo .env criado. Configure suas credenciais do banco de dados."
fi

# Construir e executar os containers
echo "🔨 Construindo containers..."
docker-compose build

echo "🚀 Iniciando serviços..."
docker-compose up -d

# Aguardar os serviços iniciarem
echo "⏳ Aguardando serviços iniciarem..."
sleep 10

# Executar migrações e seeds
echo "📊 Executando migrações e criando dados iniciais..."
docker-compose exec backend python manage.py migrate
docker-compose exec backend python seed_data.py

echo ""
echo "✅ Stockbit configurado com sucesso!"
echo ""
echo "🌐 Acesse o sistema:"
echo "   Frontend: http://localhost:5173"
echo "   Backend API: http://localhost:8000"
echo "   Admin Django: http://localhost:8000/admin"
echo ""
echo "👤 Credenciais padrão:"
echo "   Usuário: admin"
echo "   Senha: admin123"
echo ""
echo "📚 Para mais informações, consulte o README.md"
echo ""
echo "🛠️ Comandos úteis:"
echo "   make logs     - Ver logs dos serviços"
echo "   make down     - Parar os serviços"
echo "   make restart  - Reiniciar os serviços"


