# Use Python 3.10 image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy everything to the container's /app folder
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for Flask app
ENV FLASK_APP=run.py

# Expose the port that Flask uses
EXPOSE 5000

# Run the Flask app
CMD ["python3", "run.py"]
