# /opt/tdf-stack/tdf_api/Dockerfile
FROM python:3.14-slim

WORKDIR /code

# Install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy app code
COPY ./apps /code/apps

# Command to run the app (Adjust 'main:app' to your file name)
CMD ["uvicorn", "apps.main:app", "--host", "0.0.0.0", "--port", "8000"]
