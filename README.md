# relay-entry

### 

docker-compose up --build
Purpose: This command combines the building of Docker images and starting of the containers. It will build the images if there have been changes and then start the containers.
Use Case: Use this command when you want to ensure the images are up-to-date and immediately run the containers.

### 
 python3 -m venv venv
 source venv/bin/activate
 deactivate

 docker-compose restart

docker-compose down
docker-compose restart backend
docker-compose exec backend sh

# shell
docker-compose exec backend python manage.py shell

docker exec -it relay-entry-frontend-1 npm install vuetify @mdi/font

# Stripe Test Cards
Successful payment:

Card number: 4242 4242 4242 4242
Any future expiration date
Any CVC
Declined payment:

Card number: 4000 0000 0000 9995
Any future expiration date
Any CVC
Insufficient funds:

Card number: 4000 0000 0000 9995
Any future expiration date
Any CVC