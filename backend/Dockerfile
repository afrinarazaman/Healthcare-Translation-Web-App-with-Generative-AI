# Use Python 3.9 as the base image
FROM python:3.9

# Set working directory inside the container
WORKDIR /app

# Copy backend environment variables
#COPY backend/.env .env

# Copy backend requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code into the container
COPY backend/ /app

# Ensure static folder exists if required by the backend
COPY static/ /static

# Expose the port FastAPI runs on
EXPOSE 8000

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
