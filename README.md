# Event Management API
This is a Django-based API project for managing events. 
Users can register and log in, create and manage events, and register or unregister for future events. 
The project includes a token-based authentication system with token rotation, and event filtering by date, type, and status.

## Setup and Installation
### Prerequisites
- Python 3.12 or higher
- Django 5.1 or higher
- SQLite (default database)

### Installation
1) Create and activate a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```
2) Install dependencies:
```
pip install -r requirements.txt
```
3) Apply migrations:
```
python manage.py migrate
```
4) Create a superuser (for admin access):
```
python manage.py createsuperuser
```
5) Run the development server:
```
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`.

## Admin Panel
Access the Django admin panel at `http://127.0.0.1:8000/admin/` with the superuser credentials you created.

## Running Tests
To run tests for the project, use the following command:
```
python manage.py test
```

## Documentation
You can now access the Swagger UI at:
- [Swagger UI](http://127.0.0.1:8000/swagger/)

 And the ReDoc UI at:
- [ReDoc](http://127.0.0.1:8000/redoc/)