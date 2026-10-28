# Backend Project

1. Setup

Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

2. Environment variables

Copy the example file:
cp .env.example .env

Then edit .env and set values for:
- FLASK_ENV: Set to development for local development.
- SECRET_KEY: Used by Flask for sessions and security. Use a strong random string.
- DATABASE_URL: Connection string for your database.

3. Database migrations

Initialize migrations (only once):
flask db init

Generate a migration after changing models:
flask db migrate -m "Describe database changes"

Apply migrations before starting the app:
flask db upgrade