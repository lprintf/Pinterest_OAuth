# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PINTEREST_CLIENT_ID=${PINTEREST_CLIENT_ID}
ENV PINTEREST_CLIENT_SECRET=${PINTEREST_CLIENT_SECRET}
ENV PINTEREST_REDIRECT_URI=${PINTEREST_REDIRECT_URI}

# Run app.py using uvicorn with live reloading
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# docker build -t lprintf/pinterest-oauth:v0.0.1 .