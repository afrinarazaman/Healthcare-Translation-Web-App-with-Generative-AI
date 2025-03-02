# Healthcare-Translation-Web-App-with-Generative-AI
# Healthcare Translation App

The **Healthcare Translation App** is a full-stack application designed to overcome language barriers in healthcare settings. It provides accurate speech-to-text transcription, medical translation using GPT-4, and text-to-speech conversion. The backend is built with **FastAPI (Python)**, and the frontend is developed using **React**. **Docker** and **Docker Compose** are used for seamless local development and deployment to cloud services like **Render**.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Environment Variables Setup](#environment-variables-setup)
  - [Backend (.env)](#backend-env)
  - [Frontend (.env)](#frontend-env)
- [Local Development](#local-development)
- [Deployment on Render](#deployment-on-render)
- [Additional Notes](#additional-notes)

---

## Features

- **Speech Recognition & Transcription:** Uses OpenAI's Whisper API to convert speech to text.
- **Medical Translation:** Leverages GPT-4 for accurate translation with an emphasis on medical terminology.
- **Text-to-Speech Conversion:** Converts translated text into audio using Google Text-to-Speech (gTTS).
- **Secure Audio File Handling:** Encrypts and decrypts audio files to ensure secure file transfers.
- **Containerized Deployment:** Utilizes Docker and Docker Compose for local development and deployment to cloud services like Render.

---

## Project Structure

```
.
├── backend/
│   ├── __pycache__/
│   ├── Dockerfile
│   ├── app.log
│   ├── main.py
│   ├── requirements.txt
│   ├── .env  # Backend environment variables (not committed)
│
├── frontend/
│   ├── public/
│   │   ├── favicon.ico
│   │   ├── index.html
│   ├── src/
│   │   ├── app.jsx
│   │   ├── index.css
│   │   ├── index.js
│   ├── static/
│   │   ├── index.html
│   ├── Dockerfile
│   ├── package-lock.json
│   ├── package.json
│   ├── .env  # Frontend environment variables (not committed)
│
├── docker-compose.yaml
├── mock_conversation_1.wav
```

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.
- (Optional) A [Render](https://render.com/) account for deploying your app to the cloud.

---

## Environment Variables Setup

### Backend (.env)

Create a file at `backend/.env` with the following content:

```env
OPENAI_API_KEY=your_openai_api_key
ENCRYPTION_KEY=your_encryption_key
```

### Frontend (.env)

Create a file at `frontend/.env` with the following content:

```env
REACT_APP_API_URL=http://127.0.0.1:8000
REACT_APP_API_KEY=your_frontend_api_key
```

---

## Local Development

### Clone the Repository

```bash
git clone https://github.com/yourusername/healthcare-translation-app.git
cd healthcare-translation-app
```

### Set Up Environment Files

Place the `backend/.env` and `frontend/.env` files in their respective directories as described above.

### Build and Run the Containers

```bash
docker-compose down
docker-compose up --build
```

- The **backend** service will be available at: `http://127.0.0.1:8000`
- The **frontend** app will be available at: `http://127.0.0.1:3000`

---

## Deployment on Render

This project is configured for deployment on **Render** using Docker. The `Dockerfile`s for the backend and frontend are tailored for Render’s environment.

### Backend on Render

1. **Create a New Web Service on Render:**
   - Use the **Dockerfile** located in the `backend/` directory.
   - Set up environment variables from the `backend/.env` file.

### Frontend on Render

1. **Create a New Web Service on Render:**
   - Use the **Dockerfile** located in the `frontend/` directory.
   - Set build arguments for `REACT_APP_API_URL` and `REACT_APP_API_KEY`.
   - Update `REACT_APP_API_URL` to point to your backend's Render URL (e.g., `https://your-backend-service.onrender.com`).

### Frontend Dockerfile for Render

```dockerfile
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

# Expose the port
EXPOSE 3000

# Start the React app using a lightweight server
CMD ["npx", "serve", "-s", "build", "-l", "3000"]
```

---

## Additional Notes

- **Security:** Keep API keys and sensitive information secure. Do not expose them in your public repository.
- **Logs & Troubleshooting:** Use `docker-compose logs` for local troubleshooting. For Render deployments, refer to the logs available on the Render dashboard.
- **Customization:** Adjust the `docker-compose.yaml` and `Dockerfile`s as needed for your specific environment and deployment requirements.

**Happy coding! 🚀**

#### App live link: https://healthcare-translation-web-app-with-v277.onrender.com
