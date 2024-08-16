# relay-entry

Build Docker Images:

docker-compose -f docker-compose.dev.yml build
Start Services:

docker-compose -f docker-compose.dev.yml up -d
Stop Services:

docker-compose -f docker-compose.dev.yml down
View Logs:

docker-compose -f docker-compose.dev.yml logs -f
Execute Command in Running Container:

docker-compose -f docker-compose.dev.yml exec <service_name> <command>
Example:

docker-compose -f docker-compose.dev.yml exec backend python manage.py migrate
Rebuild and Restart Services:

docker-compose -f docker-compose.dev.yml up -d --build
Restart Services when .env Changes:

docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d --build

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

## Production Commands

### 1. SCP Files to Production EC2 Server

To securely copy files from your local machine to the production EC2 server, use the following command:

```bash
scp -i /path/to/your/key.pem /path/to/local/file ec2-user@ec2-instance-public-dns:/path/to/remote/directory
```

### 2. SCP Files from Production EC2 Server to Local Machine
```bash
scp -i /path/to/your/key.pem ec2-user@ec2-instance-public-dns:/path/to/remote/file /path/to/local/directory
```