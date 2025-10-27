#!/bin/bash

# Script para desenvolvimento com Docker
# Uso: ./dev.sh [comando]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir mensagens coloridas
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  Stockbit - Docker Development${NC}"
    echo -e "${BLUE}================================${NC}"
}

# Verificar se Docker está rodando
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker não está rodando. Por favor, inicie o Docker primeiro."
        exit 1
    fi
}

# Função para mostrar ajuda
show_help() {
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  start     - Inicia os serviços (frontend + backend)"
    echo "  stop      - Para os serviços"
    echo "  restart   - Reinicia os serviços"
    echo "  build     - Reconstrói as imagens"
    echo "  logs      - Mostra os logs dos serviços"
    echo "  frontend  - Apenas o frontend"
    echo "  backend   - Apenas o backend"
    echo "  clean     - Remove containers e volumes"
    echo "  prod      - Inicia em modo produção"
    echo "  help      - Mostra esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 start"
    echo "  $0 logs frontend"
    echo "  $0 build"
}

# Função principal
main() {
    print_header
    
    case "${1:-start}" in
        "start")
            print_message "Iniciando serviços de desenvolvimento..."
            check_docker
            docker-compose -f docker-compose.dev.yml up -d
            print_message "Serviços iniciados!"
            print_message "Frontend: http://localhost:5173"
            print_message "Backend: http://localhost:8000"
            print_message "Use '$0 logs' para ver os logs"
            ;;
        "stop")
            print_message "Parando serviços..."
            docker-compose -f docker-compose.dev.yml down
            print_message "Serviços parados!"
            ;;
        "restart")
            print_message "Reiniciando serviços..."
            docker-compose -f docker-compose.dev.yml restart
            print_message "Serviços reiniciados!"
            ;;
        "build")
            print_message "Reconstruindo imagens..."
            docker-compose -f docker-compose.dev.yml build --no-cache
            print_message "Imagens reconstruídas!"
            ;;
        "logs")
            if [ -n "$2" ]; then
                docker-compose -f docker-compose.dev.yml logs -f "$2"
            else
                docker-compose -f docker-compose.dev.yml logs -f
            fi
            ;;
        "frontend")
            print_message "Iniciando apenas o frontend..."
            check_docker
            docker-compose -f docker-compose.dev.yml up -d frontend
            print_message "Frontend iniciado em http://localhost:5173"
            ;;
        "backend")
            print_message "Iniciando apenas o backend..."
            check_docker
            docker-compose -f docker-compose.dev.yml up -d backend
            print_message "Backend iniciado em http://localhost:8000"
            ;;
        "clean")
            print_warning "Removendo containers, volumes e imagens..."
            docker-compose -f docker-compose.dev.yml down -v --remove-orphans
            docker system prune -f
            print_message "Limpeza concluída!"
            ;;
        "prod")
            print_message "Iniciando em modo produção..."
            check_docker
            docker-compose -f docker-compose.prod.yml up -d --build
            print_message "Serviços de produção iniciados!"
            print_message "Frontend: http://localhost"
            print_message "Backend: http://localhost:8000"
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_error "Comando desconhecido: $1"
            show_help
            exit 1
            ;;
    esac
}

# Executar função principal
main "$@"
