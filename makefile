COMPOSE=local.yml
FIG=docker-compose -f $(COMPOSE)
PROJECT_NAME=$(shell basename $(shell pwd))
RUN=$(FIG) run --rm
SERVICE=backend
SERVICE_SERVER=nginx
SERVICE_DB=db
EXEC=$(FIG) exec
BACKUP_SQL=backup.sql
TMP_SQL=tmp.sql
MANAGE=python manage.py
filename?=dev
lang?=fr
# setaf: set foreground color
RED:=$(shell tput setaf 1)
YELLOW:=$(shell tput setaf 3)
COLOR_RESET:=$(shell tput sgr0)
name:=backend

.DEFAULT_GOAL := help
.PHONY: help start stop poetry
.PHONY: build up down

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

##
## Project setup
##---------------------------------------------------------------------------

start:          ## Install and start the project
start: build up


##
## Command
##---------------------------------------------------------------------------

showcommand:	## show all personnal command
showcommand:
	$(RUN) $(SERVICE) $(MANAGE)

executecommand: ## usage: name=[command]
executecommand:
	$(EXEC) $(SERVICE) $(MANAGE) $(name)


##
## Internal rules
##---------------------------------------------------------------------------
rbuild:
	$(EXEC) $(SERVICE_SERVER) sh -c "cd frontend && npm install && npm run build && cp -R build/* /usr/share/nginx/html"

build:
	$(FIG) build

up:	## Start project container
	$(FIG) up

down: ## Stop project container
	$(FIG) down

apache-stop:
	sudo /etc/init.d/apache2 stop

tests:
	$(EXEC) $(SERVICE) sh -c "pytest"

test:
	$(EXEC) $(SERVICE) sh -c "pytest -k $(name)"

shell:
	$(EXEC) $(SERVICE) python manage.py shell

container:
	$(EXEC) $(SERVICE) sh

app:   ## make django app name=[name]
app:
	$(EXEC) $(SERVICE) bash -c "cd apps && django-admin startapp $(name)"

right-app:	## make django app with user right name=[name]
right-app: app
	sudo chown -R ${USER}:${USER} ./apps/$(name)
	$(info $(YELLOW)Don't forget to add $(name) into api/setting/base.py$(COLOR_RESET))

run-container:	## Start container
run-container:
	$(EXEC) -it $(SERVICE)


permissions:	## Give current user right on project
permissions:
	sudo chown -R ${USER}:${USER} ./


db-dump:
	$(EXEC) $(SERVICE_DB) bash -c "pg_dumpall -U postgres > backup.sql"
	docker cp $(shell docker ps --no-trunc -aqf name=a$(PROJECT_NAME)_db):/$(BACKUP_SQL) $(TMP_SQL)
	sed '/CREATE ROLE postgres;/d' ./$(TMP_SQL) > $(BACKUP_SQL)
	rm $(TMP_SQL)

force-clean:
	$(info $(RED)All images (prune) and containers (prune) will be deleted$(COLOR_RESET))
	docker container prune
	docker image prune
	docker rmi -f $(PROJECT_NAME)_backend postgres $(PROJECT_NAME)_db
	docker ps
	docker ps -a
	docker images

force-restart:	## removes images and container, rebuild, and start project
force-restart: force-clean start

db-shell:
db-shell:
	docker exec -it $(shell docker ps --no-trunc -aqf name=$(PROJECT_NAME)_db) bash

remove-images:	## remove all images and container prune + project image
remove-images:
	docker container prune
	docker image prune
	docker rmi -f $(shell docker images --no-trunc -aq $(PROJECT_NAME)_db) $(shell docker images --no-trunc -aq $(PROJECT_NAME)_backend)

remove-project:	## remove all images, container prune and remove project
remove-project: remove-images
	make permissions
	rm -Rf ../$(PROJECT_NAME) && cd ..

install: ## install all dependencies of specific file (default: dev.txt)  args: filename=[]
install:
	pip install -r requirements/$(filename).txt

translate: ## make + compile message in specific lang (default: fr)  args: lang=[]
translate:
	$(MANAGE) makemessages -l $(lang)
	$(MANAGE) compilemessages

##
## Unit Testing
##--------------------------
run-cov:
	coverage run manage.py test apps

run-cov-report: run-cov
	coverage report -m

run-cov-xml: run-cov
	coverage xml
