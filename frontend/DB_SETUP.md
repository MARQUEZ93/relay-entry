1) Delete migration files

2) Delete volumes in Docker

3) docker-compose up --build

4) docker-compose exec backend python manage.py makemigrations

5) docker-compose exec backend python manage.py migrate

6) docker-compose exec backend python manage.py shell

7) 

from django.contrib.auth.models import User
from RelayEntry.models import UserProfile

User.objects.create_superuser('root', 'example@example.com', 'p')
test1 = User.objects.create_user('test1', 'test1@example.com', 'p')
test2 = User.objects.create_user('test2', 'test2@example.com', 'p')

for user in UserProfile.objects.all():
    user.is_approved = True
    user.save()


admin / p
u / p