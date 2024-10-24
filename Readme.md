# FastAPI + MongoDB DDD CQRS Kafka FastEmail Project

This project is a backend system designed with **FastAPI** using a **MongoDB** database, applying **Domain-Driven Design (DDD)** principles, **CQRS** (Command Query Responsibility Segregation) for handling different command and query responsibilities, **Kafka** as a message broker, and **FastEmail** for email functionality. The project is fully containerized using **Docker Compose**.

## Features
- **FastAPI** for developing RESTful APIs.
- **MongoDB** as the main database.
- **DDD** (Domain-Driven Design) for clear separation of business logic.
- **CQRS** architecture to manage commands and queries.
- **Kafka** as the event streaming platform.
- **FastEmail** for sending emails.
- **Redis** for caching or message queue functionality.
- **Docker Compose** for easy setup and orchestration of the entire application stack.

## Requirements
- Docker
- Docker Compose
- `.env` file with necessary environment variables (see `.env.example`)

## Setup and Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/yourproject.git
    cd yourproject
    ```

2. Set up your environment variables:
    - Create a `.env` file based on the provided `.env.example`.
    
3. Build and start the backend services (FastAPI, Kafka):
    ```bash
    make backend_up
    ```

4. Build and start the storage services (MongoDB, Redis):
    ```bash
    make storage_up
    ```

## Makefile Commands

Here are the key `make` commands for managing the application:

### Start Backend Services
To start the **FastAPI** application and **Kafka** broker:
```bash
make backend_up
