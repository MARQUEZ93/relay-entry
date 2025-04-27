# RelayEntry

## Why RelayEntry?

I was injured, needed to get better at Django for my job & I was annoyed by RaceRoster's high transaction costs (I had paid 12% for a $30 5K lol). 

I launched a working alternative. Got a local running club in Austin, TX to successfully use it for a small race (like $1.5K in sales for a couple hundred registrants).

I'm focused on other things atm (primarily my job!) so I took it down from AWS. Making this public because why not? Any exposed keys in old commits (when the repo was closed) have been either deleted / rotated.

## Production Commands

### SCP Files to Production EC2 Server

Sometimes you have to add your IP address to the EC2 Production Security for SSH inbound rules.

To securely copy files from your local machine to the production EC2 server, use the following command:

```bash
scp -i /path/to/your/key.pem /path/to/local/file ec2-user@ec2-instance-public-dns:/path/to/remote/directory
```

### SCP Files from Production EC2 Server to Local Machine
```bash
scp -i /path/to/your/key.pem ec2-user@ec2-instance-public-dns:/path/to/remote/file /path/to/local/directory
```

### View the logger
```bash
cd relay-entry/backend/logs
tail -n 150 production.log
```

### Build Docker Image
```bash
docker-compose build
```

### Start Docker Service
```bash
docker-compose up -d
```
### Start Docker Service
```bash
docker-compose up -d
```
### SSH Onto Production EC2
```bash
ssh -i your-key-file-here.pem ec2-user@18.213.122.199 
```

### Execute Command in Running Docker Container
```bash
docker-compose exec backend python manage.py migrate
```
### Manual cerbot renewal. Start from frontend shell. Reinstall certbot due to ongoing issues.
```bash
docker exec -it relay-entry_frontend_1 sh
apk add certbot-dns-route53
certbot renew --dry-run
certbot renew
```
### Confirm cerbot renewal worked (from EC2)
```bash
sudo openssl x509 -in /etc/letsencrypt/live/relayentry.com/fullchain.pem -text -noout | grep "Not After"
```

## Local Commands

### Build / Start Docker Containers
```bash
docker-compose -f docker-compose.dev.yml up --build
```
### Execute Command in Running Docker Container 
```bash
docker-compose -f docker-compose.dev.yml exec backend python manage.py makemigrations
```
```bash
docker-compose -f docker-compose.dev.yml exec backend python manage.py migrate
```
### Activate Python3 Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Add pip package
- Manually add the package / version constraint to requirements.txt
```bash
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up --build
```
### Add npm package
```bash
docker-compose -f docker-compose.dev.yml exec frontend npm install ${package_here}
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up --build
```

## Stripe Test Cards

You can use the following test card details to simulate different payment scenarios during development. These cards work only in test mode and won't trigger actual charges.

### Successful Payment
- **Card Number**: `4242 4242 4242 4242`
- **Expiration Date**: Any future date (e.g., `12/34`)
- **CVC**: Any 3-digit number (e.g., `123`)

### Declined Payment
- **Card Number**: `4000 0000 0000 9995`
- **Expiration Date**: Any future date (e.g., `12/34`)
- **CVC**: Any 3-digit number (e.g., `123`)

### Insufficient Funds
- **Card Number**: `4000 0000 0000 9995`
- **Expiration Date**: Any future date (e.g., `12/34`)
- **CVC**: Any 3-digit number (e.g., `123`)

> **Note**: For more test card numbers and scenarios, please refer to [Stripe's official documentation](https://stripe.com/docs/testing).
