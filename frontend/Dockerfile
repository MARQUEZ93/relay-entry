# Use the official Node.js image from the Docker Hub
FROM node:14

# Set work directory
WORKDIR /app

COPY ./package.json ./
RUN npm install
COPY . .

# Expose the port that the app runs on
EXPOSE 8080

# Run the application
CMD ["npm", "run", "serve"]
