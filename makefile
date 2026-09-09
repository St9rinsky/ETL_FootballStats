REGISTRY := docker.io
IMAGE_NAME := zuyasjhb025/robot-worlds-server
IMAGE := $(REGISTRY)/$(IMAGE_NAME):$(tag)

.PHONY: \
	daemon-start \
	daemon-stop \
    build \
	run \
	rebuild \
	stop \
	logs \
	shell \
	help

daemon-start:
	docker desktop start

daemon-stop:
	docker desktop stop

build: daemon-start
	docker compose build

run: daemon-start
	docker compose up

rebuild: daemon-start
	docker compose up --build

stop:
	docker compose down
	daemon-stop

logs:
	docker compose logs -f

shell:
	docker compose exec football-etl bash

help:
	@echo "make build      → Build image"
	@echo "make run        → Run ETL"
	@echo "make rebuild    → Rebuild and run image"
	@echo "make stop       → Stop containers"
	@echo "make logs       → See logs"
	@echo "make shell      → Enter container"