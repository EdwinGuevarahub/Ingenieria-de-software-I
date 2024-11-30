# Presentacion Examen
Dev Docker Environment

# Containers
	- database(PostgreSQL)
	- backend(django rest framework)
	- frontend(reactjs)

# Useful commands
	- docker compose up (-d detached mode);
	- docker compose down -v ; docker rmi -f $(docker images -aq);
	- docker-compose down && docker volume prune -f && docker-compose up --build -d
	- docker system prune;
# Execution command
	- docker compose down -v && docker compose up --build
