# relay-entry

### 

docker-compose up --build

### 
 python3 -m venv venv
 source venv/bin/activatede
 deactivate

 docker-compose exec backend python manage.py createsuperuser
 docker-compose exec relay-entry-backend-1 python manage.py migrate
 docker-compose exec relay-entry-backend-1 python manage.py createsuperuser


root / p