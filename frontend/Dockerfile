# Use Node.js as the base image
FROM node:18

# Set working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy all files from the current context
COPY . .

# Pass build arguments into environment variables for the React app
ARG REACT_APP_API_URL
ARG REACT_APP_API_KEY
ENV REACT_APP_API_URL=${REACT_APP_API_URL}
ENV REACT_APP_API_KEY=${REACT_APP_API_KEY}

# Build the React app
RUN npm run build

# Expose the port (Render will assign it dynamically)
EXPOSE 3000

# Ensure "serve" is installed and use dynamic PORT from Render
RUN npm install -g serve
CMD ["sh", "-c", "serve -s build -l ${PORT:-3000}"]
