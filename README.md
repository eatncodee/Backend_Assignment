# ⚡ Real-Time Task Monitor

An asynchronous, high-performance backend service built with FastAPI that provides secure, real-time task management. This started as a personal project and was extended to include role-based access control (user/admin) and an admin dashboard — alongside the original OAuth2/JWT authentication, Redis-backed rate-limited login, and WebSocket-based real-time synchronization.

## 🚀 Key Features

* **Role-Based Access Control:** Distinct `user` and `admin` roles enforced at the API level. Users manage their own tasks; admins can view all tasks across every user and perform bulk operations.
* **Real-Time Synchronization:** Utilizes WebSockets and a centralized `ConnectionManager` to push instant task updates (create, update, delete) to all active client sessions.
* **Secure Authentication:** Implements OAuth2 with Password Bearer, using `bcrypt` for password hashing and `JWT` (JSON Web Tokens) for secure, stateless API access. Role is embedded in the token payload.
* **Rate Limiting:** Redis-backed login rate limiter restricts repeated failed attempts per IP, capped at 5 attempts per 60-second window.
* **Asynchronous Database Operations:** Fully non-blocking CRUD operations utilizing MongoDB with the `Motor` async driver.
* **Data Privacy & Ownership:** Strict endpoint-level validation ensures authenticated users can only view, modify, and delete their own tasks.
* **RESTful Architecture:** Clean, versioned REST APIs (`/api/v1/`) for standard data operations alongside the real-time WebSocket pipeline.
* **API Documentation:** Interactive Swagger UI available at `/docs` and ReDoc at `/redoc`.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Framework:** FastAPI
* **Real-Time:** WebSockets, Asyncio
* **Database:** MongoDB (Motor Async Driver)
* **Cache / Rate Limiting:** Redis
* **Security:** OAuth2, JWT (python-jose), bcrypt (passlib)
* **Data Validation:** Pydantic v2
* **Frontend:** Vanilla JS (served via FastAPI static files)
* **Package Manager:** uv

## 📁 Project Structure

```
app/
├── routes/
│   ├── auth.py        # Login endpoint
│   ├── user.py        # Register, /me
│   ├── task.py        # Task CRUD + admin endpoints
│   └── ws.py          # WebSocket endpoint
├── schema/
│   └── schema.py      # Pydantic models
├── db/
│   └── db.py          # MongoDB connection
├── frontend/
│   └── index.html     # Vanilla JS frontend
├── Oauth2.py          # JWT logic, get_current_user, require_admin
├── SocketManager.py   # WebSocket ConnectionManager
├── redis_dependency.py# Rate limiter
└── main.py            # App entry point
```

## 🔐 API Endpoints

### Authentication
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/api/v1/register` | Public | Register with email, password, role |
| POST | `/api/v1/login` | Public | Returns JWT access token |

### Tasks
| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | `/api/v1/alltasks` | User | Get current user's tasks |
| POST | `/api/v1/task` | User | Create a new task |
| PUT | `/api/v1/tasks/{id}` | User | Update a task |
| DELETE | `/api/v1/tasks/{id}` | User | Delete a task |
| GET | `/api/v1/admin/tasks` | Admin | Get all tasks across all users |
| DELETE | `/api/v1/all-tasks` | Admin | Delete every task in the database |

### WebSocket
| Endpoint | Description |
|----------|-------------|
| `ws://localhost:8000/ws?token=<jwt>` | Real-time task event stream |

## ⚙️ Architecture Highlight: The Connection Manager

To handle real-time broadcasts efficiently, this project implements a Singleton-style `ConnectionManager`. It acts as a centralized, in-memory switchboard that tracks all active user WebSocket sessions. When a task is mutated via a REST endpoint, the manager immediately broadcasts the new state to the specific user's connected devices, ensuring perfectly synchronized UIs without database polling.

## 🏃 Running the Project

1. Clone the repo and create a `.env` file in the root:
```
mongo_uri=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/
```

2. Start Redis (required for rate limiting):
```bash
docker run -d -p 6379:6379 redis
```

3. Install dependencies and run:
```bash
uv sync
uv run uvicorn app.main:app --reload
```

4. Open `http://localhost:8000` for the frontend or `http://localhost:8000/docs` for Swagger.
