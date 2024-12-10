FROM python:3.13-slim

# Install system dependencies needed for psycopg2 and other required packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    && apt-get clean

# Set the working directory
WORKDIR /app

# Copy the app directory to the container
COPY ./app /app

# Upgrade pip and install the required Python packages
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Start the application
CMD ["python", "app.py"]
