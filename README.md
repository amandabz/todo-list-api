# Todo List API

A RESTful API for managing personal to-do lists with user authentication, built with FastAPI and PostgreSQL.

## Tech Stack

- **FastAPI** — web framework
- **SQLModel** — ORM and data validation
- **PostgreSQL** — database (via Docker)
- **JWT** — authentication tokens
- **passlib + bcrypt** — password hashing
- **uv** — package manager

## Getting Started

### Prerequisites

- Python 3.14+
- Docker

### Setup

1. Clone the repository and navigate to the project folder.

2. Copy the environment file and fill in the values:
   ```bash
   cp .env.example .env
   ```

   ```env
   DB_PASSWORD=your_password
   DB_NAME=todo_db
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/todo_db
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

3. Start the database:
   ```bash
   docker compose up -d
   ```

4. Install dependencies:
   ```bash
   uv sync
   ```

5. Run the API:
   ```bash
   uv run fastapi dev
   ```

The API will be available at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

## API Endpoints

### Auth

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/register` | Register a new user | No |
| POST | `/login` | Login and get token | No |

### Todos

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/todos/` | Create a todo | Yes |
| GET | `/todos/` | Get all todos (paginated) | Yes |
| GET | `/todos/{id}` | Get a single todo | Yes |
| PUT | `/todos/{id}` | Update a todo | Yes |
| DELETE | `/todos/{id}` | Delete a todo | Yes |

### Authentication

All todo endpoints require a Bearer token in the `Authorization` header:

```
Authorization: Bearer <token>
```

### Pagination

The `GET /todos/` endpoint supports pagination via query params:

```
GET /todos/?page=1&limit=10
```

Response:
```json
{
  "data": [...],
  "page": 1,
  "limit": 10,
  "total": 25
}
```

## Error Responses

| Status | Meaning |
|--------|---------|
| 400 | Bad request (e.g. email already exists) |
| 401 | Unauthorized (missing or invalid token) |
| 403 | Forbidden (todo belongs to another user) |
| 404 | Todo not found |

## Testing with Bruno

The `todo_list/` folder contains a Bruno collection with all the requests ready to use.

1. Open Bruno and click **Open Collection**, select the `todo_list/` folder.
2. Set the active environment to **local**.
3. In the **Register user** and **Login user** requests, go to **Script → Post Response** and add the following script to automatically save the token:
   ```javascript
   var data = res.getBody();
   bru.setEnvVar("token", data.token);
   ```
4. Run **Register user** or **Login user** — the token will be saved to `{{token}}` automatically.
5. All todo requests use `{{token}}` as the Bearer token, so they will work without any manual copy-pasting.

## Database

To inspect the database directly:

```bash
docker exec -it todo_postgres psql -U postgres -d todo_db
```

To stop the database without losing data:
```bash
docker compose stop
```

To remove everything including data:
```bash
docker compose down -v
```

## Project Information
This project is based on the [Todo List API](https://roadmap.sh/projects/todo-list-api?fl=0) from **roadmap.sh**.
