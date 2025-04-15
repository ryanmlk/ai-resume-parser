# Stage 1: Build the React frontend
FROM node:23 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/ ./
RUN npm install && npm run build

# Stage 2: Set up Python backend
FROM python:3.12-slim AS backend
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev

WORKDIR /app

# Copy backend code and install dependencies
COPY backend/ ./backend/
COPY backend/requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy frontend build into backend static directory
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Expose the port and run
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host=0.0.0.0", "--port=80"]
