# Use an official Python runtime as the base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /BackendD

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /BackendD
COPY . .

# Expose port 8000 for HTTP and 8001 for WebSocket
EXPOSE 8000
EXPOSE 8001

# Run Daphne for WebSocket and HTTP requests
CMD ["sh", "-c", "daphne -b 0.0.0.0 -p 8001 BackendD.asgi:application & python manage.py runserver 0.0.0.0:8000"]
