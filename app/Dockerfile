# Use the official Python image from Docker Hub
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt if it exists, otherwise create an empty file
COPY requirements.txt* /app/ || touch /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app

# Set environment variables (optional)
ENV APP_ENV=production

# Expose the port the app runs on
EXPOSE 5000

# Command to run the app (adjust as needed)
CMD ["python", "run.py"]
