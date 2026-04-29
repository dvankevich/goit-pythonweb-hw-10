## goit-pythonweb-hw-08
Simple contactlist CRUD API
### run project
```bash
git clone https://github.com/dvankevich/goit-pythonweb-hw-08
cd goit-pythonweb-hw-08/
```
#### set database credentials in .env file
```bash
cp env.example .env
```

```
POSTGRES_USER=<postgres_username>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<database_name>
POSTGRES_HOST=<hostname or IP address>
POSTGRES_PORT=<port. default 5432>
```
#### Generate a secure JSON Web Token (JWT) secret key by
```bash
openssl rand -base64 32
```
set JWT parameters in .env file
```
JWT_SECRET=<secret_key>
JWT_ALGORITHM=HS256"
JWT_EXPIRATION_SECONDS=3600
```
#### create database via CLI
```bash
psql -U postgres # if postgesql in your host

docker exec -it <container_name> psql -U postgres # if posgresql in docker container
```

```sql
CREATE DATABASE contacts_db WITH ENCODING = 'UTF8';

\q
```
#### install packages
```bash
poetry install
```
#### activate virtual env
```bash
poetry env use 3.13
eval $(poetry env activate)
```
#### run database migrations
```bash
alembic upgrade head
```

#### run in dev-mode
```bash
fastapi dev main.py
```

Server started at http://127.0.0.1:8000

Documentation at http://127.0.0.1:8000/docs

### build docker container
```bash
docker build -t hw10-fastapi-app .
```

### run app docker container with postgesql on host
```bash
docker run -d \
  --name contacts-fastapi-app \
  -p 8000:8000 \
  --add-host=host.docker.internal:host-gateway \
  --env-file .env \
  -e POSTGRES_HOST=host.docker.internal \
  hw10-fastapi-app
```
#### view logs
```bash
docker logs -f contacts-fastapi-app
```
#### remove container
```bash
docker rm -f contacts-fastapi-app
```