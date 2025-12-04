# Overview of this bookshelf
This task is a standard, fundamental step in Django development that involves creating a specific feature (a **Book** model) within an isolated part of the project (the bookshelf app) and preparing it to interact with a database.

## 1. The Role of the bookshelf App
A Django project is a collection of settings and configurations, while a **Django app** is a standalone, reusable module that handles a specific function.

**Command**: python3 manage.py startapp bookshelf

**Result**: This creates a new subdirectory named bookshelf with its own set of files (models.py, views.py, admin.py, etc.).

**Purpose**: The bookshelf app is where all the logic, models, and views related to managing books will reside, keeping the code clean and modular.

## 2. Defining the Book Model in models.py
The **Model** is the definitive source of truth about your data. It contains the essential fields and behaviors of the data you're storing.

**Location**: bookshelf/models.py

**Concept**: By creating the Book class, you are telling Django, and specifically the Object-Relational Mapper (ORM), how to structure a corresponding table in your database (e.g., SQLite, PostgreSQL).


|field name      | Django Field Type         | Database Column Type |  Purpose
_______________________________________________________________________________
|  title         | CharField(max_length=200) | VARCHAR(200)         | Stores the book's title as text, limited to 200 characters.
|  author        | CharField(max_length=100) | VARCHAR(100)         | Stores the author's name, limited to 100 characters.
|publication_year| IntegerField              | INTEGER              | Stores the year of publication as a whole number.
