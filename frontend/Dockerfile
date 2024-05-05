# Use official Node.js as a parent image
FROM node:lts-alpine

# Set work directory
WORKDIR /app

# Install Vue CLI globally
RUN npm install -g @vue/cli

# Create a new Vue project (This will use default presets. For custom configuration, this step should be run interactively or modify as needed)
RUN vue create frontend -d

# Expose the port Vue CLI serve runs on
EXPOSE 8080

# Command to serve the app
CMD ["npm", "run", "serve"]