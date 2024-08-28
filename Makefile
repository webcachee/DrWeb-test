DC = docker compose
EXEC = docker exec -it
APP_CONTAINER = flask-app
DOCKER_FILE = docker-compose.yml
LOGS = docker logs
ENV = --env-file .env

.PHONY: app app-down app-logs run-test

app:
	${DC} -f ${DOCKER_FILE} ${ENV} up --build -d

app-down:
	${DC} -f ${DOCKER_FILE} down

app-logs:
	${LOGS} ${APP_CONTAINER} -f

run-test:
	${EXEC} ${APP_CONTAINER} pytest
