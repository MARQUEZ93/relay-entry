# Database

### Local DB Setup

1) Delete volumes in Docker

2) Build app
```bash
docker-compose -f docker-compose.dev.yml up --build
```

3) Run Migrations
```bash
docker-compose -f docker-compose.dev.yml exec backend python manage.py migrate
```

4) Enter the Django Shell
```bash
docker-compose -f docker-compose.dev.yml exec backend python manage.py shell
```

5) Create admin user & event director users

```
from django.contrib.auth.models import User
from RelayEntry.models import UserProfile

User.objects.create_superuser('root', 'example@example.com', 'p')
test1 = User.objects.create_user('test1', 'test1@example.com', 'p')
test2 = User.objects.create_user('test2', 'test2@example.com', 'p')

for user in UserProfile.objects.all():
    user.is_approved = True
    user.save()
```