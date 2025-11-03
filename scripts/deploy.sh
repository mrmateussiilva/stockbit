#!/bin/bash

# Script de deploy simplificado para StockBit
# Uso: ./scripts/deploy.sh

set -e

echo "🚀 Iniciando deploy do StockBit..."
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar se está no diretório correto
if [ ! -f "docker-compose.simple.yml" ]; then
    echo -e "${RED}❌ Erro: Execute este script no diretório raiz do projeto${NC}"
    exit 1
fi

# Verificar se .env.production existe
if [ ! -f ".env.production" ]; then
    echo -e "${YELLOW}⚠️  Arquivo .env.production não encontrado!${NC}"
    echo "Criando a partir do exemplo..."
    if [ -f ".env.production.example" ]; then
        cp .env.production.example .env.production
        echo -e "${YELLOW}⚠️  IMPORTANTE: Edite .env.production com suas configurações antes de continuar!${NC}"
        exit 1
    else
        echo -e "${RED}❌ Erro: .env.production.example não encontrado${NC}"
        exit 1
    fi
fi

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker não está instalado!${NC}"
    exit 1
fi

# Verificar Docker Compose
if ! docker compose version &> /dev/null; then
    echo -e "${RED}❌ Docker Compose não está instalado!${NC}"
    exit 1
fi

echo "✅ Pré-requisitos verificados"
echo ""

# Perguntar se quer fazer backup
read -p "Deseja fazer backup do banco antes? (s/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo "💾 Fazendo backup do banco..."
    BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
    docker compose -f docker-compose.simple.yml exec -T db pg_dump -U stockbit stockbit > "$BACKUP_FILE" 2>/dev/null || echo "⚠️  Não foi possível fazer backup (banco pode não estar rodando)"
    if [ -f "$BACKUP_FILE" ]; then
        echo -e "${GREEN}✅ Backup criado: $BACKUP_FILE${NC}"
    fi
fi

echo ""
echo "🔨 Construindo imagens..."
docker compose -f docker-compose.simple.yml build

echo ""
echo "🚀 Iniciando containers..."
docker compose -f docker-compose.simple.yml up -d

echo ""
echo "⏳ Aguardando containers ficarem prontos..."
sleep 10

echo ""
echo "✅ Verificando status dos containers..."
docker compose -f docker-compose.simple.yml ps

echo ""
echo -e "${GREEN}✅ Deploy concluído!${NC}"
echo ""
echo "📊 Próximos passos:"
echo "  1. Verifique os logs: docker compose -f docker-compose.simple.yml logs -f"
echo "  2. Crie um superusuário: docker compose -f docker-compose.simple.yml exec web python manage.py createsuperuser"
echo "  3. Acesse o sistema no seu navegador"
echo ""

