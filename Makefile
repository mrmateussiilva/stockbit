# Makefile para o projeto Stockbit

.PHONY: up down build logs clean restart

# Comandos principais
up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose up --build -d

restart:
	docker-compose restart

logs:
	docker-compose logs -f

# Comandos de desenvolvimento
logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

# Comandos de banco de dados
migrate:
	docker-compose exec backend python manage.py migrate

makemigrations:
	docker-compose exec backend python manage.py makemigrations

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

# Comandos de limpeza
clean:
	docker-compose down -v
	docker system prune -f

clean-all:
	docker-compose down -v --rmi all
	docker system prune -af

# Comandos de shell
shell-backend:
	docker-compose exec backend python manage.py shell

shell-frontend:
	docker-compose exec frontend sh

# Comandos de teste
test:
	docker-compose exec backend python manage.py test

# Comandos de coleta de arquivos estáticos
collectstatic:
	docker-compose exec backend python manage.py collectstatic --noinput

