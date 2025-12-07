# /opt/tdf-stack/tdf_api/Dockerfile
FROM python:3.14-slim

WORKDIR /code

# Install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy app code
COPY ./apps /code/apps

# Command to run the app (Adjust 'main:app' to your file name)
<<<<<<< HEAD
CMD ["uvicorn", "apps.main:app", "--host", "0.0.0.0", "--port", "8000"]
=======
CMD ["uvicorn", "apps.main:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> 5f6412a3478bbe6c893979d4fc2487a698c4750a
