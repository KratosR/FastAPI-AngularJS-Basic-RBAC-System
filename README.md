# 🚀 Role-Based Access Control System – Full Stack Application

[FastAPI](https://img.shields.io/badge/FastAPI-0.115.8-009688?style=flat&logo=fastapi) + [JWT](https://img.shields.io/badge/JWT-Auth-000000?style=flat&logo=json-web-tokens) + [MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql) + [Angular](https://img.shields.io/badge/Angular-18.0.0-DD0031?style=flat&logo=angular) + [Bootstrap](https://img.shields.io/badge/Bootstrap-5.0.0-7952B3?style=flat&logo=bootstrap)

**A complete full‑stack RBAC (Role‑Based Access Control) system with JWT authentication, role hierarchy, and full CRUD operations. Built with FastAPI (backend) and Angular + Bootstrap (frontend).**

## Features

### 🔐 Authentication & Authorization
- JWT‑based authentication (access token)
- Role hierarchy: admin → instructor → student
- Password hashing with bcrypt
- Protected routes with role‑based guards (frontend & backend)

### 👥 User Management
- Full CRUD for users (admin only)
- Self‑profile update (any authenticated user)
- Cascade delete of user → removes associated student/instructor record

### 🎭 Role Management
- Create, list, delete roles (admin only)
- Self‑referential parent‑child relationship
- Prevents deletion of roles with children or assigned users

### 🎓 Student Management
- Instructors: Create, read, update students
- Admins: All instructor actions + DELETE students
- Students have no write access

### 👨‍🏫 Instructor Management
- Admins only: Create, read, update, delete instructors

### 🖥️ Frontend Dashboard
- Role‑based navigation (admin / instructor / student)
- Bootstrap 5 responsive UI
- Font Awesome icons
- Reactive forms with validation

### High -Level Overview of Application

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│   Angular 17    │  ─────► │    FastAPI      │  ─────► │     MySQL       │
│ (localhost:4200)│   JWT   │ (localhost:8000)│   SQL   │   Database      │
└─────────────────┘         └─────────────────┘         └─────────────────┘
         │                           │
         └───── Proxy (dev) ─────────┘
              or CORS (prod)
```

## Prerequisites

- Python 3.11+
- Node.js 18+ & npm 9+
- Angular CLI 18+ (npm install -g @angular/cli)
- MySQL 8.0 (or MariaDB)
- Git (optional)

## Installation

1. Clone the repository

2. Create Virtual Enviroment :
```bash
### Python + FastAPI

# Create virtual environment
python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows
```

3. Install Dependencies
```env
# Install dependencies
pip install -r requirements.txt
```

4. Connect DB using .env
```env
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=your_port
DB_NAME=DB_NAME
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. Create Database, Tables & Seed Data
```bash
# Run Setup Command
python -m scripts.cli initdb

# Run Server
uvicorn app.main:app --reload
```

5. Run these commands
```bash
### AngularJS

# Install dependencies
npm install or update

# Run Project
npm start
```

6. Now Backend is running on (http://localhost:8000), (http://localhost:8000/docs) & Frontend is running on (http://localhost:4200).