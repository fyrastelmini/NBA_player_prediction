run:
	docker-compose up
stop:
	docker-compose down --volumes --remove-orphans
	docker system prune -a -f