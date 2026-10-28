# ShopStack — Product Catalog & Cart System

ShopStack is a full-stack e-commerce project built to explore Python backend development, REST APIs, microservices, database integration, and containerization. It provides a product catalog with stock management and a persistent shopping cart through separate backend services.

## Features

- **Product Catalog:** View products, prices, stock availability, and product images.
- **Product Management API:** Create, retrieve, update, and delete products.
- **Stock Management:** Automatically reduce product stock when an item is added to the cart.
- **Shopping Cart:** Add products, view cart items, and remove individual products.
- **Cart Persistence:** Store cart items in PostgreSQL so they survive frontend refreshes and Cart Service restarts.
- **REST API Integration:** Connect the React frontend to the backend services.
- **Dockerized Environment:** Run the backend services and PostgreSQL using Docker Compose.

## Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite, CSS |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| HTTP Communication | REST APIs, HTTPX |
| API Testing | Postman |
| Containerization | Docker, Docker Compose |
| Testing | Pytest |
| Version Control | Git, GitHub |

## Architecture

ShopStack uses separate services for product management and cart operations.

```text
React + TypeScript Frontend
          |
          | REST API requests
          |
     +----+----+
     |         |
     v         v
Product API  Cart Service
:8000        :8001
     |         |
     |         +----> Product API
     |                (stock updates)
     +---------+
           |
           v
       PostgreSQL
```

- **Product Service:** Manages product records, product images, and stock quantities.
- **Cart Service:** Manages cart items and communicates with the Product Service to update stock.
- **PostgreSQL:** Stores product information and persistent cart records.
- **Frontend:** Displays the product catalog and shopping cart.

## Project Structure

```text
shopstack/
├── cart_service/
│   ├── app.py
│   ├── db.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   │   └── images/
│   └── src/
├── tests/
├── app.py
├── db.py
├── product_repository.py
├── schemas.py
├── compose.yaml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

Install the following tools before running the project:

- Python 3.11+
- Node.js and npm
- Docker Desktop
- Git

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd shopstack
```

Replace `<YOUR_GITHUB_REPOSITORY_URL>` with your repository URL.

### 2. Configure environment variables

Create a `.env` file in the project root using the variables expected by `db.py` and `compose.yaml`.

Example:

```env
DB_USER=postgres
DB_PASSWORD=your_local_password
DB_HOST=localhost
DB_PORT=5433
DB_NAME=shopstack_restore
```

Use your own local password. **Do not commit `.env` or real credentials to GitHub.**

Docker Compose overrides the database host and port for the API and Cart Service so they can connect to PostgreSQL using the internal Docker network.

### 3. Start the backend services and database

From the project root, run:

```bash
docker compose up -d --build
```

Check the running containers:

```bash
docker compose ps
```

View logs if needed:

```bash
docker compose logs --tail=50 api
docker compose logs --tail=50 cart
```

The database must contain the required `products` and `cart_items` tables. Use the project's existing database setup and schema before testing the application.

### 4. Start the frontend

Open a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local Vite URL displayed in the terminal, usually:

http://localhost:5173

## API Endpoints

### Product Service — `http://localhost:8000`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/products` | Retrieve all products |
| GET | `/products/{product_id}` | Retrieve a product by ID |
| POST | `/products` | Create a product |
| PUT | `/products/{product_id}` | Update a product |
| DELETE | `/products/{product_id}` | Delete a product |
| POST | `/products/{product_id}/reduce-stock` | Reduce product stock |

Interactive API documentation is available at:

http://localhost:8000/docs

### Cart Service — `http://localhost:8001`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/cart/{user_id}` | Retrieve a user's cart |
| POST | `/cart/{user_id}/items` | Add an item to the cart |
| DELETE | `/cart/{user_id}/items/{product_id}` | Remove an item from the cart |

Interactive API documentation is available at:

http://localhost:8001/docs

*Confirm endpoint paths against the current service code if you change the routes.*

## Running Tests

Run the automated tests from the project root:

```bash
python -m pytest
```

The current test suite contains four tests. All four passed in the latest local test run.

## Testing with Postman

You can use Postman to test the backend APIs:

1. Retrieve products using `GET /products`.
2. Create or update a product.
3. Add a product to a user's cart.
4. Verify that stock decreases after adding the item.
5. Retrieve the cart and verify its contents.
6. Remove one product and confirm other cart items remain.

## Future Improvements

- Add automated integration tests for the Cart Service.
- Add authentication and user-specific cart management.
- Improve transaction handling between stock updates and cart database writes.
- Add CI workflows for automated testing.
- Add deployment configuration and production environment settings.

## Learning Outcomes

This project provided practical experience with:

- Building REST APIs using FastAPI.
- Connecting Python services to PostgreSQL.
- Separating product and cart functionality into services.
- Integrating a React and TypeScript frontend with backend APIs.
- Managing application dependencies with Docker Compose.
- Writing and running automated tests with Pytest.

## Author

**Mrudula V.**

GitHub: https://github.com/mrudulav19
