# Stage 1: Build the Vue.js application
FROM node:18-alpine as build

# Install essential packages including Certbot, DNS Route53 plugin for AWS, and cron
RUN apk update && apk add --no-cache bash curl certbot certbot-dns-route53 cronie

# Set work directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json ./
COPY package-lock.json ./
 
# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build
RUN echo "Dockerfile build stage was hit!"

# Stage 2: Serve the application with Nginx
FROM nginx:alpine
# Install cron in the Nginx container
RUN apk add --no-cache bash curl certbot cronie

EXPOSE 80
EXPOSE 443
# Copy built assets from the build stage
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

# Set up the cron job for Certbot renewal
RUN echo "0 */12 * * * certbot renew --quiet --deploy-hook \"nginx -s reload\"" > /etc/crontabs/root

# Start cron and Nginx
CMD ["sh", "-c", "crond && nginx -g 'daemon off;'"]
