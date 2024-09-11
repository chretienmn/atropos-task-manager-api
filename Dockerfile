# Base image: Official Python 3.9 image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements file first for layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Set AWS Environment variables
ENV AWS_ACCESS_KEY_ID=testing
ENV AWS_SECRET_ACCESS_KEY=testing
ENV AWS_DEFAULT_REGION=us-east-1

# Expose port 8000 for the Falcon API
EXPOSE 8000

# Command to run the app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:api"]
