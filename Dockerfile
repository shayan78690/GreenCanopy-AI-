FROM python:3.9-slim

# Set environment variables for best practice
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Set the working directory
WORKDIR /app

# Copy only the requirements first (so pip installs are cached if unchanged)
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . /app

# Expose port 80
EXPOSE 80

# Run your app with uvicorn (for FastAPI)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
