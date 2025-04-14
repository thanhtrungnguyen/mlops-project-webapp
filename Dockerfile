# Use a lightweight Python image
FROM python:3.12.10-slim

# Set a working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire repo into /app
COPY . .

# Expose the Flask port
EXPOSE 5000

# Default command
CMD ["python", "app/app.py"]
