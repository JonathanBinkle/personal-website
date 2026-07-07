docker-prune:
	# prunes <none> images, build cache, etc.
	# helpful to reclaim space on hard disk and to start from scratch
	@docker system prune -a

docker-pull:
	@if [ -e .env ]; then rm .env; fi
	@ln -s .env.prod .env
	@docker compose -f compose.prod.yaml build --pull

setup-dev: .env.dev
	@if [ -e .env ]; then rm .env; fi
	@ln -s .env.dev .env
	@docker compose up --build -d

setup-prod: .env.prod
	@if [ -e .env ]; then rm .env; fi
	@ln -s .env.prod .env
	@docker compose -f compose.prod.yaml up --build -d

teardown-dev:
	@docker compose down

teardown-prod:
	@docker compose -f compose.prod.yaml down

test:
	@for app in core blog; do \
		docker exec portfolio-django python /home/django/www/manage.py test $$app --no-input --verbosity 2; \
	done

prune-unused-images-volumes:
	docker image prune -f
	docker volume prune -f

create-backup:
	@mkdir -p backup
	@docker exec portfolio-mysql-prod sh -c 'exec mysqldump $$MYSQL_DATABASE -uroot -p"$$MYSQL_ROOT_PASSWORD" --compact' > backup/dump.sql
	@docker cp -a portfolio-nginx-prod:/home/django/mediafiles backup
	@tar -czf ../backup-$(shell date '+%Y-%m-%d').tar.gz backup --remove-files
	
restore-backup:
	@mkdir -p backup
	# Restore the most recent backup in case there are multiple
	@tar -xzf $(shell ls -1 ../backup-*.tar.gz | sort -r -n | head -n 1) -C backup/ --strip-components=1
	@if [ $$? -eq 0 ]; then \
		echo "SET FOREIGN_KEY_CHECKS=0;" > tmp_dump.sql; \
		cat backup/dump.sql >> tmp_dump.sql; \
		echo "SET FOREIGN_KEY_CHECKS=1;" >> tmp_dump.sql; \
		cat tmp_dump.sql > backup/dump.sql; \
		rm tmp_dump.sql; \
		docker exec -i portfolio-mysql-prod sh -c 'exec mysql -uroot -p"$$MYSQL_ROOT_PASSWORD" -e "DROP DATABASE IF EXISTS $$MYSQL_DATABASE; CREATE DATABASE $$MYSQL_DATABASE;"'; \
		docker exec -i portfolio-mysql-prod sh -c 'exec mysql $$MYSQL_DATABASE -uroot -p"$$MYSQL_ROOT_PASSWORD"' < backup/dump.sql; \
		docker exec -i portfolio-nginx-prod sh -c 'rm -rf /home/django/mediafiles/*'; \
		docker cp -a backup/mediafiles/. portfolio-nginx-prod:/home/django/mediafiles/.; \
		rm -rf backup; \
		echo "\n>>> Done <<<"; \
	else \
		@echo "\n>>> ERROR: Extraction of backup failed <<<"; \
	fi

enable-maintenance:
	@docker cp ./nginx/error_pages/maintenance.html portfolio-nginx-prod:/etc/nginx/error_pages/maintenance.html

disable-maintenance:
	@docker exec portfolio-nginx-prod rm /etc/nginx/error_pages/maintenance.html

reload-gunicorn:
	# Command substitution as in 'kill -HUP $(pgrep ...)' doesn't work! Use xargs.
	@docker exec -it portfolio-django-prod sh -c 'pgrep gunicorn | head -n 1 | xargs -r kill -HUP'

rebuild-%:
	@docker compose -f compose.prod.yaml up --build -d $*
