DOCKER_USERNAME ?= kpn
APPLICATION_NAME ?= datasource

run:
	docker build --tag ${DOCKER_USERNAME}/${APPLICATION_NAME} .
	docker container run -p 8000:8000 ${DOCKER_USERNAME}/${APPLICATION_NAME}
