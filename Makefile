.PHONY: up down logs build migrate shell-api shell-db test-api lint

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

build:
	docker compose build

migrate:
	docker compose exec api alembic upgrade head

shell-api:
	docker compose exec api bash

shell-db:
	docker compose exec db psql -U mailmind mailmind

test-api:
	docker compose exec api pytest -v

lint-api:
	docker compose exec api ruff check app/

lint-web:
	docker compose exec web npm run lint

fresh: down
	docker compose up -d --build
	sleep 5
	docker compose exec api alembic upgrade head
