# 🚀 Project Overview: LibraryProject

This project is a foundational **Django application** named `LibraryProject`, designed to demonstrate a basic Django development environment setup.

## 🛠️ Setup and Environment

The goal of this initial setup was to establish the core Django project structure and ensure the local development server is operational.

  * **Framework:** Django
  * **Initial Setup:** Django was installed using `pip install django`.
  * **Project Creation:** The project was created with `django-admin startproject LibraryProject`.

## ▶️ Getting Started

To run the project locally:

1.  **Navigate** to the `LibraryProject` directory:
    ```bash
    cd LibraryProject
    ```
2.  **Start** the development server:
    ```bash
    python manage.py runserver
    ```
3.  **View** the application at `http://127.0.0.1:8000/`.

## 📂 Core Structure

Key files to note within the project structure:

  * **`manage.py`**: A command-line utility for interacting with the project (e.g., running the server, migrations).
  * **`settings.py`**: Contains the project's configuration (database, installed apps, middleware, etc.).
  * **`urls.py`**: Defines the project's URL patterns (the "table of contents" for the site).