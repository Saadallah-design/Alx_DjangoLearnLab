# Project Overview
In the “Introduction to Building APIs with Django REST Framework” project, you will learn to create and manage RESTful APIs using Django REST Framework (DRF). This project is tailored for you to understand the core concepts of API development with DRF, including setting up a new Django project, creating serializers, viewsets, and implementing authentication and permissions. By the end of this project, you will have the foundational skills needed to build robust APIs with Django REST Framework.

## Learning Objectives
### By the end of this project, you will be able to:

* Set Up a New Django Project with Django REST Framework:

* Create a new Django project and configure it to use Django REST Framework.
Set up a basic environment for API development, including creating models and running migrations.
Build Your First API Endpoint with Django REST Framework:

* Develop a simple API endpoint to retrieve data using serializers and views in DRF.
Understand the core components of DRF, including serializers and generic views.
Implement CRUD Operations with ViewSets and Routers in Django REST Framework:

* Use DRF’s ViewSets and Routers to simplify the implementation of CRUD operations.
Manage standard database operations through RESTful APIs effectively.
Implement Authentication and Permissions in Django REST Framework:

* Secure API endpoints by implementing authentication schemes and permission settings.
Ensure only authorized users can access and modify data through the API.

### Step 1: Create a ViewSet
ViewSets in DRF allow you to consolidate common logic for handling standard operations into a single class that handles all HTTP methods (GET, POST, PUT, DELETE).

## Tasks for next time
### 🚀 Next Steps: Finalizing the API and User Setup
Before starting development, I need to finalize the database structure and create an initial user. 
Specifically: 
* 1) Delete the problematic migration file from api/migrations/. 
* 2) Temporarily update the author field in api/models.py to null=True to allow the migration to run successfully without a user. 
* 3) Execute python manage.py makemigrations api and python manage.py migrate to apply the Foreign Key constraint. 
* 4) Finally, run python manage.py createsuperuser to add the first user, which is necessary to test the Token Authentication and the IsAuthorOrReadOnly permissions enforced by your BookViewSet. After creation, you may optionally remove null=True from your model and run migrations again.

