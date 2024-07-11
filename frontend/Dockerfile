# Stage 1: Build the Vue.js application
FROM node:14 AS build

# Set work directory
WORKDIR /app

# Copy package.json and package-lock.json (if using npm)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# List the contents of the dist directory (for debugging)
RUN echo "Contents of /app/dist:" && ls /app/dist && echo "Build stage completed."

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

# Copy built assets from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

# List the contents of the html directory (for debugging)
RUN echo "Contents of /usr/share/nginx/html:" && ls /usr/share/nginx/html && echo "Nginx stage completed."

# Expose the port that Nginx runs on
EXPOSE 80

# The default command for Nginx is to run the server, no need to override it
