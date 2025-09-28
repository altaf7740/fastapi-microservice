include .env
export $(shell sed 's/=.*//' .env)

generate-migrations:
	uv run alembic -c src/alembic.ini revision --autogenerate -m "message"

migrate:
	uv run alembic -c src/alembic.ini upgrade head

bypass-precommit:
	@echo "Skipping pre-commit hook"
	git commit --no-verify


#######################################################
# Don't run below command inside docker               #
#######################################################

app-build-dev:
	docker build -t $(APP_IMAGE_NAME) --target dev .

app-run-dev:
	docker run --name $(APP_CONTAINER_NAME) --rm --env-file .env \
		-p 8000:8000 -v .:/root/project $(APP_IMAGE_NAME)

app-build:
	docker build -t $(APP_IMAGE_NAME) --target prod .

app-run:
	docker run --name $(APP_CONTAINER_NAME) --rm --env-file .env \
		-p 8000:8000 $(APP_IMAGE_NAME)