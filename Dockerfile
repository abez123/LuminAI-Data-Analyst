# -------- Step 1: Base Node image for React Development --------
FROM node:18-alpine AS frontend-dev

WORKDIR /app

# Copy package.json and install dependencies
COPY ./package.json ./vite.config.ts ./tsconfig.json ./tsconfig.app.json ./eslint.config.js ./package-lock.json* ./
RUN npm install

# Copy the source code
COPY ./src ./src
COPY ./public ./public

# Install 'nodemon' for hot-reloading during development
RUN npm install -g nodemon

# Command to start Vite development server
CMD ["npm", "run", "dev"]

# -------- Step 2: Base Python image for FastAPI Development --------
FROM python:3.11-slim AS backend-dev

WORKDIR /app

# Copy backend-specific files
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend code
COPY ./backend .

# -------- Step 3: Final setup for running dev environments --------
# Using the base Python image
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH=/app

# Copy FastAPI backend
COPY --from=backend-dev /app /app

# Install Node.js and NPM for frontend dev
RUN apt-get update && apt-get install -y nodejs npm

# Copy frontend files
COPY --from=frontend-dev /app /app

# Install any missing Python packages (if necessary)
COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI and frontend ports
EXPOSE 5174

# Command to start FastAPI development server
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]