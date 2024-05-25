# Use the official Node.js image from the Docker Hub
FROM node:14

# Set work directory
WORKDIR /app

# Copy package.json first
COPY package.json /app/

# Install dependencies (and generate package-lock.json)
RUN npm install

# Copy project files
COPY . /app/

# Expose the port that the app runs on
EXPOSE 8080

# Run the application
CMD ["npm", "run", "serve"]
