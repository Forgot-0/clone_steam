DC = docker compose
BACKEND_APP = docker_compose/app.yaml
STORAGE = docker_compose/storage.yaml
BROKER = docker_compose/broker.yaml
REDIS = docker_compose/redis.yaml
ENV = --env-file .env


.PHONY: backend_up
backend_up:
	${DC} -f ${BACKEND_APP} -f ${BROKER} ${ENV} up -d --build

.PHONY: backend_down
backend_down:
	${DC} -f ${BACKEND_APP} -f ${BROKER} ${ENV} down

.PHONY: storage_up
storage_up:
	${DC} -f ${STORAGE} -f ${REDIS} ${ENV} up -d --build

.PHONY: storage_down
storage_down:
	${DC} -f ${STORAGE} -f ${REDIS} ${ENV} down

.PHONY: app_down
app_down:
	${DC} -f ${BACKEND_APP} -f ${STORAGE} -f ${REDIS} -f ${BROKER} ${ENV} down