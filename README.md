# Backend Project

A Flask REST API with JWT authentication, user-owned tasks, PostgreSQL, database migrations, and

 Docker Compose.

1. Setup

Clone the repository and enter the project directory:

git clone YOUR_REPOSITORY_URL

cd backend-project

Create and activate a virtual environment:

python3 -m venv venv

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

2. Environment variables

Copy the example environment file:

cp .env.example .env

Edit .env and set a secure JWT_SECRET

EX:

JWT_SECRET=replace-with-a-long-random-secret 

DATABASE_URL=sqlite:///dev.db

-JWT_SECRET: Secret used to sign. and verify JWT authentication tokens. Use a strong, private

 value.

-DATABASE_URL: Database connection string. The application defaults to SQLite for local

 development. Docker Compose supplies the PostgreSQL connection string to the web container.

Generate a secure JWT secret with:

python3 -c "import secrets; print(secrets.token_hex(32))"

Never commit your actual .env file or share your secrets.

3. Database migrations

For a fresh clone, apply the existing migrations:

docker compose --env-file .env -f backend_project/docker-compose.yml exec web flask --app

 'backend_project:create_app("development")' db upgrade

When you change database models, generate and apply a migration:

docker compose --env-file .env -f backend_project/docker-compose.yml exec web flask --app 

'backend_project:create_app("development")' db migrate -m "Describe database changes"

docker compose --env-file .env -f backend_project/docker-compose.yml exec web flask --app 

'backend_project:create_app("development")' db upgrade

4. Run with Docker Compose

Make sure Docker Desktop is running.

Build the image and start the application and PostgreSQL database:

docker compose --env-file .env -f backend_project/docker-compose.yml up --build -d

Check that the containers are running:

docker compose --env-file .env -f backend_project/docker-compose.yml ps

Apply database migrations inside the web container:

docker compose --env-file .env -f backend_project/docker-compose.yml exec web flask --app 

'backend_project:create_app("development")' db upgrade

The API is available at:

http://localhost:8000

5. Verify the API

Health check

curl -i http://localhost:8000/health

Expected response: HTTP 200 with a successful status.

Register a user

curl -i -X POST http://localhost:8000/register \
-H "Content-Type: application/json" \
-d '{"username":"testuser","email":"test@example.com","password":"TestPassword123"}'

Expected response: HTTP 201.

Log in

curl -i -X POST http://localhost:8000/login \
-H "Content-Type: application/json" \
-d '{"email":"test@example.com","password":"TestPassword123"}'

Expected response: HTTP 200 with an access_token.

Create a task

Replace YOUR_ACCESS_TOKEN with the token returned by login:

curl -i -X POST http://localhost:8000/tasks \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
-d '{"title":"My first task"}'

Expected response: HTTP 201.

List tasks

curl -i http://localhost:8000/tasks \
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"

Expected response: HTTP 200 with the authenticated user's tasks.

6. Stop the containers

Stop the application and database:

docker compose --env-file .env -f backend_project/docker-compose.yml down

PostgreSQL data is stored in a named Docker volume and is preserved when containers are stopped or recreated.

Warning: Adding -v to the docker compose down command removes the named volume and deletes the stored database data.