# Use Node.js as the base image
FROM node:18

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json and install dependencies
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Copy public and src folders into the container
COPY frontend/public ./public
COPY frontend/src ./src

# Pass build arguments into environment variables for the React app
ARG REACT_APP_API_URL
ARG REACT_APP_API_KEY
ENV REACT_APP_API_URL=${REACT_APP_API_URL}
ENV REACT_APP_API_KEY=${REACT_APP_API_KEY}

# Build the React app
RUN npm run build

# Expose the port
EXPOSE 3000

# Start the React app using a lightweight server
CMD ["npx", "serve", "-s", "build", "-l", "3000"]
