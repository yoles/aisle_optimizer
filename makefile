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
build:	## Build project container
build:
	$(FIG) build

up:	## Start project container
up: apache-stop
	$(FIG) up

down: ## Stop project container
	$(FIG) down

start: ## Install and start the project
start: build up

##
## Internal rules
##---------------------------------------------------------------------------
apache-stop:	## Stop apache to free port 80
	sudo /etc/init.d/apache2 stop

permissions:	## Give current user right on project
permissions:
	sudo chown -R ${USER}:${USER} ./

force-clean:	## Remove All dangling images and containers + project images
force-clean:
	$(info $(RED)All images (prune) and containers (prune) will be deleted$(COLOR_RESET))
	docker container prune
	docker image prune
	docker rmi -f $(PROJECT_NAME)_$(SERVICE) $(PROJECT_NAME)_$(SERVICE_SERVER)
	docker ps
	docker ps -a
	docker images

force-restart: ## removes images and container, rebuild, and start project
force-restart: force-clean start

remove-project:	## remove all images, container prune and remove project
remove-project: force-clean
	$(info $(RED) [WARNING] $(PROJECT_NAME) will be removed $(COLOR_RESET))
	@read -p "Are you sure you want to continue ? (y/n) " confirmation; \
	confirmation=$$(echo $$confirmation | tr '[:upper:]' '[:lower:]'); \
	if [ "$$confirmation" = "yes" ] || [ "$$confirmation" = "y" ] || [ "$$confirmation" = "oui" ] || [ "$$confirmation" = "o" ]; then \
		make permissions \
		rm -Rf ../$(PROJECT_NAME) && cd .. \
		echo "Fichier supprimé."; \
	else \
		echo "Suppression annulée."; \
	fi

##
## Backend Command
##---------------------------------------------------------------------------
showcommand:	## show all personnal command
showcommand:
	$(RUN) $(SERVICE) $(MANAGE)

executecommand: ## usage: name=[command]
executecommand:
	$(EXEC) $(SERVICE) $(MANAGE) $(name)

tests:
	$(EXEC) $(SERVICE) sh -c "pytest"

test:
	$(EXEC) $(SERVICE) sh -c "pytest -k $(name)"

flake8:
	$(EXEC) $(SERVICE) sh -c "flake8 ."

black:
	$(EXEC) $(SERVICE) sh -c "black api apps"

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

install: ## install all dependencies of specific file (default: dev.txt)  args: filename=[]
install:
	pip install -r requirements/$(filename).txt

translate: ## make + compile message in specific lang (default: fr)  args: lang=[]
translate:
	$(MANAGE) makemessages -l $(lang)
	$(MANAGE) compilemessages

##
## Frontend Command
##---------------------------------------------------------------------------
rbuild:
	$(EXEC) $(SERVICE_SERVER) sh -c "cd frontend && npm install && npm run build && cp -R build/* /usr/share/nginx/html"

##
## Frontend Command
##---------------------------------------------------------------------------
db-dump:
	$(EXEC) $(SERVICE_DB) bash -c "pg_dumpall -U postgres > backup.sql"
	docker cp $(shell docker ps --no-trunc -aqf name=a$(PROJECT_NAME)_db):/$(BACKUP_SQL) $(TMP_SQL)
	sed '/CREATE ROLE postgres;/d' ./$(TMP_SQL) > $(BACKUP_SQL)
	rm $(TMP_SQL)

db-shell:
db-shell:
	docker exec -it $(shell docker ps --no-trunc -aqf name=$(PROJECT_NAME)_db) bash


##
## Unit Testing
##--------------------------
run-cov:
	coverage run manage.py test apps

run-cov-report: run-cov
	coverage report -m

run-cov-xml: run-cov
	coverage xml
