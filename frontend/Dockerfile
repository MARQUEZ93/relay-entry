# Stage 1: Build the Vue.js application
FROM node:14 as build

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

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

EXPOSE 80
# Copy built assets from the build stage
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

# Expose the port that Nginx will run on
# CMD ["nginx", "-g", "daemon off;"]
