# Use the official Node.js image
FROM node:18

# Create and change to the backend directory
WORKDIR /usr/src/app

# Install dependencies
COPY package*.json ./
RUN npm install

# Install Docker CLI
RUN apt-get update && apt-get install -y docker.io

# Copy the rest of the application code
COPY . .

# Expose the backend port
EXPOSE 5000

# Run the application
CMD ["npm", "start"]