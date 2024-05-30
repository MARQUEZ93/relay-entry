# relay-entry

### 

docker-compose up --build

### 
 python3 -m venv venv
 source venv/bin/activatede
 deactivate

 docker-compose exec backend python manage.py migrate
 docker-compose exec backend python manage.py createsuperuser

 docker-compose exec backend python manage.py makemigrations backend

 docker-compose restart

 docker-compose down


root / p
# shell
docker-compose exec backend python manage.py shell