![Python](https://img.shields.io/badge/python-3.14-blue)
![Django](https://img.shields.io/badge/django-6.x-green)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

## A Django REST Framework project that replicates the Star Wars API (SWAPI), using local data storage and URL-based relationships instead of foreign keys. 

Rest Api for: 
- Planets
- Films
- Species
- Starships
- Vehicles
- Characters

Import services and django command for full import.

Testing.

Swagger.

### Tech Stack 

- Python
- Django
- Django Rest Framework
- SQLite
- Drf-spectacular (Swagger docs)

### Setup

1. Clone the repository
   ```
   git clone https://github.com/GeorgeDurieux/swapi-clone.git
   cd swapi
   ```
2. Create virtual environment
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies
   ```
   pip install -r requirements.txt
   ```
4. Environmental variables
   ```
   BASE_URL=http://localhost:8000/api
   SWAPI_URL=https://swapi.dev/api
   ```
5. Run migrations
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
6. (Optional) Import SWAPI data
   - Enter shell
      ```
      python manage.py shell
      ```
   - Import data
     ```
     python manage.py import_swapi
     ```

7. Run the project
   ```
   python manage.py runserver
   ```

### Documentation

Swagger available at
```
http://localhost:8000/api/docs/
```

### Author
George Durieux

### Licence
MIT License
      
     

