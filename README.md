⚡ Real-Time Task Monitor

An asynchronous, high-performance backend service built with FastAPI that provides secure, real-time task management. The application features robust OAuth2/JWT authentication and utilizes WebSockets to broadcast instant state synchronization across multiple connected clients without the need for HTTP polling.

## 🚀 Key Features

* **Real-Time Synchronization:** Utilizes WebSockets and a centralized `ConnectionManager` to push instant task updates (create, update, delete) to all active client sessions.
* **Secure Authentication:** Implements OAuth2 with Password Bearer, using `bcrypt` for password hashing and `JWT` (JSON Web Tokens) for secure, stateless API access.
* **Asynchronous Database Operations:** Fully non-blocking CRUD operations utilizing MongoDB with the `Motor` async driver.
* **Data Privacy & Ownership:** Strict endpoint-level validation ensures authenticated users can only view, modify, and manage their own specific tasks.
* **RESTful Architecture:** Clean, well-documented REST APIs for standard data fetching alongside the real-time WebSocket pipeline.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Framework:** FastAPI
* **Real-Time:** WebSockets, Asyncio
* **Database:** MongoDB (Motor Async Driver)
* **Security:** OAuth2, JWT (PyJWT), bcrypt (passlib)
* **Data Validation:** Pydantic

## ⚙️ Architecture Highlight: The Connection Manager

To handle real-time broadcasts efficiently, this project implements a Singleton-style `ConnectionManager`. It acts as a centralized, in-memory switchboard that tracks all active user WebSocket sessions. When a task is updated via a REST endpoint, the manager immediately broadcasts the new state to the specific user's connected devices, ensuring perfectly synchronized UIs without database polling.