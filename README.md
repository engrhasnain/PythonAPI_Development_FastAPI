# 🚀 FastAPI CRUD API Project

This project demonstrates building **RESTful APIs using FastAPI** for performing CRUD operations with **both raw SQL queries** and **SQLAlchemy ORM models**.  
It also includes **Pydantic models** for data validation and leverages **PostgreSQL** as the database backend.

---

## 🧠 What I Learned

- Building and structuring **FastAPI applications** for clean and scalable APIs.  
- Performing **CRUD (Create, Read, Update, Delete)** operations:
  - Using **raw SQL queries**.
  - Using **SQLAlchemy ORM** for a more Pythonic database interaction.
- Defining **Pydantic models** for request and response validation.
- Managing database connections with **SQLAlchemy session** and **engine**.
- Working with **PostgreSQL** using the `psycopg2` driver.
- Organizing project structure into separate modules for:
  - `models/` → SQLAlchemy models
  - `database/` → Connection and session setup  
  - `main.py` → FastAPI app and routes

---

## ⚙️ Tech Stack

- **FastAPI** – Modern, async Python web framework  
- **SQLAlchemy** – ORM for database operations  
- **Pydantic** – Data validation and serialization  
- **PostgreSQL** – Relational database  
- **psycopg2** – PostgreSQL database adapter for Python  

