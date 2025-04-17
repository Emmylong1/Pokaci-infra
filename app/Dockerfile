# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app/

# Handle optional requirements.txt
RUN test -f requirements.txt || touch requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Expose port (optional, based on your app)
EXPOSE 5000

# Run Flask app
CMD ["python", "run.py"]
