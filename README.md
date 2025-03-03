# Healthcare Translation App

The Healthcare Translation App is a full-stack application designed to overcome language barriers in healthcare settings. It provides accurate speech-to-text transcription, medical translation using GPT-4, and text-to-speech conversion. The backend is built with FastAPI (Python) and the frontend with React. Containerization using Docker and Docker Compose enables seamless local development as well as cloud deployment (e.g., on Render).

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
- [CI/CD Using GitHub Actions](#cicd-using-github-actions)
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
│   ├── main.py                  # FastAPI backend code
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile                # Backend Dockerfile
│   ├── .env                      # Backend environment variables (not included in GitHub)
│
├── frontend/
│   ├── public/
│   │   ├── favicon.ico
│   │   ├── index.html
│   ├── src/
│   │   ├── app.jsx
│   │   ├── index.js
│   │   ├── index.css
│   ├── Dockerfile                # Dockerfile for Render deployment
│   ├── package.json              # React app dependencies
│   ├── package-lock.json
│   ├── .env                      # Frontend environment variables (not included in GitHub)
│
├── docker-compose.yaml            # Docker Compose file for local development
```
---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.
- (Optional) A [Render](https://render.com/) account for deploying your app to the cloud.

---

## Environment Variables Setup

### Backend (.env)

Create a file at `backend/.env` with the following content (replace the example values with your own):

```env
API_KEY=your_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
ENCRYPTION_KEY=your_encryption_key_here
```

### Frontend (.env)

Create a file at `frontend/.env` with the following content:

```env
REACT_APP_API_KEY=your_api_key_here
REACT_APP_API_URL=http://127.0.0.1:8000
```

---

## Local Development

### Clone the Repository

```bash
git clone https://github.com/afrinarazaman/Healthcare-Translation-Web-App-with-Generative-AI.git
cd Healthcare-Translation-Web-App-with-Generative-AI
```

### Set Up Environment Files

Place the `backend/.env` and `frontend/.env` files in their respective directories as described above.

### Build and Run the Containers

Use the following Docker Compose commands:

```bash
docker-compose down
docker-compose up --build
```

- The **backend** service will be available at: `http://127.0.0.1:8000`
- The **frontend** app will be available at: `http://127.0.0.1:3000`

---

## Deployment on Render

### Backend on Render

Create a **New Web Service** on Render:
- Use the Dockerfile located in the `backend/` directory.
- Set the build and runtime environment variables using the values in your `backend/.env` file.

### Frontend on Render

Your frontend Dockerfile for Render is already uploaded to GitHub, so simply create a **New Web Service** on Render and link it to your GitHub repository.

For deployment on Render, update the **`REACT_APP_API_URL`** to point to your backend's Render URL (e.g., `https://your-backend-service.onrender.com`).

---

## CI/CD Using GitHub Actions

To automate testing and deployment, you can use GitHub Actions. Below is a sample `.github/workflows/deploy.yml` workflow for building and deploying both backend and frontend to Render.

### Example GitHub Actions Workflow (`.github/workflows/deploy.yml`):

```yaml
name: Deploy to Render

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Build and push Docker images
      run: |
        docker build -t my-backend-image ./backend
        docker build -t my-frontend-image ./frontend

    - name: Deploy to Render
      env:
        RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
      run: |
        curl -X POST "https://api.render.com/v1/services/my-backend-service/deploys" -H "Authorization: Bearer $RENDER_API_KEY"
        curl -X POST "https://api.render.com/v1/services/my-frontend-service/deploys" -H "Authorization: Bearer $RENDER_API_KEY"
```

### Steps in the Workflow:
1. **Trigger:** Runs when changes are pushed to the `main` branch.
2. **Checkout:** Pulls the latest repository code.
3. **Docker Build:** Builds the Docker images for both backend and frontend.
4. **Deploy:** Triggers a deployment on Render using the Render API.

To use this workflow, add your **Render API Key** as a GitHub Secret (`RENDER_API_KEY`).

---

## Additional Notes

- **Security:** Keep API keys and sensitive information secure. Do not expose them in your public repository.
- **Logs & Troubleshooting:** Use `docker-compose logs` for local troubleshooting. For Render deployments, refer to the logs available on the Render dashboard.
- **Customization:** Feel free to adjust the Docker Compose file and Dockerfiles as needed for your specific environment and deployment requirements.

🚀 **Happy coding!**
