# Use the official Python image as the base image
FROM python:3.8

# Set environment variables for Python and Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=UTC

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files to the working directory
COPY gg_backend /app/gg_backend
COPY requirements.txt /app/

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app will run on
EXPOSE 5000

# Define the entry point for the container
CMD ["flask", "run", "--host=0.0.0.0"]
