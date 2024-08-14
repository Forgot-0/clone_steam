DC = docker compose
BACKEND_APP = docker_compose/app.yaml
STORAGE = docker_compose/storage.yaml
BROKER = docker_compose/broker.yaml
ENV = --env-file .env


.PHONY: backend_up
backend_up:
	${DC} -f ${BACKEND_APP} -f ${BROKER} ${ENV} up -d --build

.PHONY: bakend_down
bakend_down:
	${DC} -f ${BACKEND_APP} -f ${BROKER} ${ENV} down


.PHONY: storage_up
storage_up:
	${DC} -f ${STORAGE} ${ENV} up -d --build

.PHONY: storege_down
storege_down:
	${DC} -f ${STORAGE} ${ENV} down


.PHONY: app_down
app_down:
	${DC} -f ${BACKEND_APP} -f ${STORAGE} ${ENV} down