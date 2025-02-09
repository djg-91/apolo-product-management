# Base image
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Expose ports for Product Manager (8000) and Order Manager (8001)
EXPOSE 8000
EXPOSE 8001

# Default command (overridden by docker-compose)
CMD ["sh", "-c", "echo 'Use docker-compose to run the containers'"]