# ShopStack

A backend product catalog API built with Python, FastAPI, and PostgreSQL, containerized using Docker and Docker Compose.

## Features

- Create, retrieve, update, and delete products (CRUD).
- PostgreSQL database integration using `psycopg`.
- Request validation using Pydantic.
- REST API testing with Postman.
- Automated tests using `pytest`.
- Dockerized API and PostgreSQL services.
- Persistent PostgreSQL storage using a Docker volume.
- Environment-based configuration for database credentials.

## Tech Stack

- **Language:** Python
- **API:** FastAPI, Uvicorn
- **Database:** PostgreSQL
- **Database Driver:** psycopg
- **Validation:** Pydantic
- **Testing:** pytest, Postman
- **Containerization:** Docker, Docker Compose
- **Version Control:** Git and GitHub

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API availability |
| GET | `/products` | Retrieve products |
| POST | `/products` | Create a product |
| PUT | `/products/{product_id}` | Update a product |
| DELETE | `/products/{product_id}` | Delete a product |

## Run with Docker Compose

### Prerequisites

- Docker Desktop
- Git

### Setup

1. Clone this repository:

   ```bash
   git clone <YOUR_GITHUB_REPOSITORY_URL>
   cd shopstack
   ```

2. Create a `.env` file in the project root with your local database configuration:

   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=shopstack_db
   DB_USER=postgres
   DB_PASSWORD=your_local_password
   ```

   Use your own credentials. Never commit `.env` to GitHub.

3. Start the application:

   ```bash
   docker compose up -d --build
   ```

4. Open the interactive API documentation:

   http://127.0.0.1:8000/docs

5. Check the products endpoint:

   http://127.0.0.1:8000/products

### Stop the application

```bash
docker compose down
```

The PostgreSQL data is stored in a named Docker volume, so stopping the services this way does not delete the database volume.

## Testing

Run the existing automated tests from your Python environment:

```bash
pytest -v
```

The API's CRUD endpoints can also be tested using the ShopStack API collection in Postman.

## Project Structure

```text
shopstack/
├── app.py
├── db.py
├── product_repository.py
├── schemas.py
├── main.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .gitignore
├── tests/
└── README.md
```

## Learning Goals

This project is being developed to practise backend API development, relational database integration, automated testing, containerization, and deployment fundamentals. Future improvements may include microservices and Kubernetes.

## Security Notes

- Keep `.env` and database backups out of version control.
- Use environment variables for credentials.
- Do not use development credentials in production.
