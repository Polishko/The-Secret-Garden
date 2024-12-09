# Use a slim Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Set the command to run Gunicorn
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "thesecretgarden.wsgi:application"]
