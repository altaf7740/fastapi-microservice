include .env
export $(shell sed 's/=.*//' .env)




#######################################################
# Don't run below command inside docker               #
#######################################################

app-build:
	docker build -t $(APP_IMAGE_NAME) --target dev .

app-run:
	docker run --name $(APP_CONTAINER_NAME) --rm --env-file .env \
		-p 8000:8000 -v $(shell pwd)/src:/root/project/src $(APP_IMAGE_NAME)
