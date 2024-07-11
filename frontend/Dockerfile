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

# Debugging step: List the contents of /app before building
RUN echo "Contents of /app before building:" && ls -l /app

# Build the application
RUN npm run build

# List the contents of the dist directory (for debugging)
RUN echo "Contents of /app/dist:" && ls /app/dist && echo "Build stage completed."

# Stage 2: Serve the application with Nginx
FROM nginx:alpine

# Debugging step: List files before copying
RUN echo "Before copying, contents of /usr/share/nginx/html:" && ls -l /usr/share/nginx/html

# Copy built assets from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Debugging step: List the contents of the html directory
RUN echo "After copying, contents of /usr/share/nginx/html:" && ls -l /usr/share/nginx/html

# Expose the port that Nginx runs on
EXPOSE 80

# The default command for Nginx is to run the server, no need to override it
