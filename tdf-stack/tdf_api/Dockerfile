# /opt/tdf-stack/tdf_api/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Command to run the app (Adjust 'main:app' to your file name)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]