#!/bin/bash

# Script para gerenciar o ambiente de produção do Stockbit

set -e

# Escolher qual compose usar (caddy ou nginx direto)
if [ -f "docker-compose.prod-caddy.yml" ] && [ -z "$USE_NGINX" ]; then
    PROD_COMPOSE="docker-compose -f docker-compose.prod-caddy.yml"
    echo "Usando configuração com Caddy"
else
    PROD_COMPOSE="docker-compose -f docker-compose.prod.yml"
    echo "Usando configuração com Nginx direto"
fi

case "$1" in
    start)
        echo "🚀 Iniciando serviços de produção..."
        $PROD_COMPOSE up -d
        echo "✅ Serviços iniciados com sucesso!"
        ;;
    
    stop)
        echo "🛑 Parando serviços de produção..."
        $PROD_COMPOSE stop
        echo "✅ Serviços parados!"
        ;;
    
    restart)
        echo "🔄 Reiniciando serviços de produção..."
        $PROD_COMPOSE restart
        echo "✅ Serviços reiniciados!"
        ;;
    
    build)
        echo "🔨 Construindo imagens de produção..."
        $PROD_COMPOSE build
        echo "✅ Imagens construídas!"
        ;;
    
    build-no-cache)
        echo "🔨 Construindo imagens de produção (sem cache)..."
        $PROD_COMPOSE build --no-cache
        echo "✅ Imagens construídas!"
        ;;
    
    logs)
        $PROD_COMPOSE logs -f ${2:-}
        ;;
    
    ps)
        $PROD_COMPOSE ps
        ;;
    
    down)
        echo "⚠️  Removendo containers de produção..."
        $PROD_COMPOSE down
        echo "✅ Containers removidos!"
        ;;
    
    down-volumes)
        echo "⚠️  Removendo containers e volumes de produção..."
        $PROD_COMPOSE down -v
        echo "✅ Containers e volumes removidos!"
        ;;
    
    shell-backend)
        $PROD_COMPOSE exec backend sh
        ;;
    
    shell-db)
        $PROD_COMPOSE exec db psql -U stockbit_user stockbit_db
        ;;
    
    createsuperuser)
        echo "👤 Criando superusuário..."
        $PROD_COMPOSE exec backend python manage.py createsuperuser
        ;;
    
    migrate)
        echo "🗄️  Aplicando migrações..."
        $PROD_COMPOSE exec backend python manage.py migrate
        ;;
    
    backup)
        BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
        echo "💾 Fazendo backup do banco de dados..."
        $PROD_COMPOSE exec -T db pg_dump -U stockbit_user stockbit_db > $BACKUP_FILE
        echo "✅ Backup criado: $BACKUP_FILE"
        ;;
    
    update)
        echo "🔄 Atualizando sistema de produção..."
        git pull
        $PROD_COMPOSE build
        $PROD_COMPOSE up -d
        echo "✅ Sistema atualizado!"
        ;;
    
    *)
        echo "📦 Stockbit - Gerencial Sistema de Produção"
        echo ""
        echo "Uso: ./prod.sh [comando]"
        echo ""
        echo "Comandos disponíveis:"
        echo "  start              Iniciar serviços"
        echo "  stop               Parar serviços"
        echo "  restart            Reiniciar serviços"
        echo "  build              Construir imagens"
        echo "  build-no-cache     Construir imagens (sem cache)"
        echo "  logs [serviço]     Ver logs (ex: logs backend)"
        echo "  ps                 Ver status dos serviços"
        echo "  down               Remover containers"
        echo "  down-volumes       Remover containers e volumes"
        echo "  shell-backend      Acessar shell do backend"
        echo "  shell-db           Acessar shell do banco de dados"
        echo "  createsuperuser    Criar usuário administrador"
        echo "  migrate            Aplicar migrações"
        echo "  backup             Fazer backup do banco de dados"
        echo "  update             Atualizar sistema (git pull + build)"
        echo ""
        exit 1
        ;;
esac

