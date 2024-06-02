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
docker-compose restart backend


root / p
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