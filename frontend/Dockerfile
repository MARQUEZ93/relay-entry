# Use the official Node.js image from the Docker Hub
FROM node:14

# Set work directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json /app/

# Install dependencies
RUN npm install

# Copy project files
COPY . /app/

# Expose the port that the app runs on
EXPOSE 8080

# Run the application
CMD ["npm", "run", "serve"]
