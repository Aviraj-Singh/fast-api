# FastAPI Backend Learning Project

This repository contains my step-by-step journey of learning backend development using FastAPI. The project evolves from basic API creation to building a real-world backend system with database integration, relationships, and authentication.

## Overview

The goal of this project is to build a strong backend foundation by implementing concepts from scratch instead of relying on tutorials. Each stage builds on the previous one, simulating how real backend systems are developed.

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- Pydantic
- Bcrypt (for password hashing)

### Core API Development
- REST APIs (GET, POST, PUT, DELETE)
- Request and response validation using Pydantic
- Proper HTTP status codes
- Error handling using custom exceptions

### Project Structure
- Modular architecture with separation of concerns:
  - routes
  - models
  - dependencies
  - exceptions
  - config
- Dependency Injection using FastAPI Depends

### Database Integration
- PostgreSQL setup using Docker
- Database connection management
- ORM using SQLAlchemy
- CRUD operations with persistent storage

### Data Modeling
- User and Item models
- One-to-many relationship (User → Items)
- Foreign key implementation
- ORM relationships using relationship()

### API Design
- Nested routes:
  - Create item for user: `/users/{user_id}/items`
  - Fetch user items: `/users/{user_id}/items`
- Clean and scalable API structure

### Data Integrity
- Cascade delete (deleting a user removes associated items)
- Validation checks (duplicate users, duplicate items per user)

### Security Foundations
- Password hashing using bcrypt via passlib
- Avoiding plain text password storage

## Folder Structure

```
project/
│
├── routes/
│   ├── users.py
│   ├── items.py
│
├── models/
│   ├── base.py
│   ├── user.py
│   ├── item.py
│   ├── schemas.py
│
├── dependencies/
│   ├── database.py
│
├── exceptions/
│
├── utils/
│   ├── security.py
│
├── config.py
├── main.py
```

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/Aviraj-Singh/fast-api
cd fast-api
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3. Run PostgreSQL using Docker
```bash
docker run -d \
  --name postgres-db \
  -e POSTGRES_USER=username \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=db_name \
  -p 5432:5432 \
  postgres
```

### 4. Set environment variables

Create a `.env` file:

```env
DB_URL=postgresql://username:password@localhost:5432/db_name
SECRET_TOKEN=your_secret_key
```

### 5. Run the server
```bash
uvicorn main:app --reload
```

### 6. Access API docs
```
http://127.0.0.1:8000/docs
```

## Learning Highlights

- Transitioned from in-memory data to real database systems
- Understood how backend systems manage data persistence
- Learned how relationships define system structure
- Implemented real-world patterns like dependency injection and modular architecture
- Built APIs that reflect actual product-level backend design
- Implemented authentication using JWT

## Next Steps

- Add authorization and role-based access
- Introduce database migrations using Alembic
- Add middleware and logging
- Optimize performance and scalability
