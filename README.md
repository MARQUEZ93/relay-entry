# relay-entry

### 

docker-compose up --build
Purpose: This command combines the building of Docker images and starting of the containers. It will build the images if there have been changes and then start the containers.
Use Case: Use this command when you want to ensure the images are up-to-date and immediately run the containers.

### 
 python3 -m venv venv
 source venv/bin/activatede
 deactivate

 docker-compose exec backend python manage.py migrate
 docker-compose exec backend python manage.py createsuperuser

 docker-compose exec backend python manage.py makemigrations

 docker-compose restart

 docker-compose down
docker-compose restart backend


admin / p
u / p
# shell
docker-compose exec backend python manage.py shell

# Create superuser, two users in shell
from django.contrib.auth.models import User
from RelayEntry.models import UserProfile

User.objects.create_superuser('admin', 'example@example.com', 'p')
test1 = User.objects.create_user('test1', 'test1@example.com', 'p')
test2 = User.objects.create_user('test2', 'test2@example.com', 'p')

make all UserProfiles is_approved
for user in UserProfile.objects.all():
    user.is_approved = True
    user.save()


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