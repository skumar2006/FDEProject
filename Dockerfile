FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create data directory and copy data files
RUN mkdir -p /app/data
COPY data/* /app/data/

# Use environment variable for port with default fallback
ENV PORT=8080

# Expose the port the app runs on
EXPOSE ${PORT}

# Command to run the application with dynamic port
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT} 