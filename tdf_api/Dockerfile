FROM python:3.12-slim

WORKDIR /app

COPY tdf_api/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY tdf_utility/ /app/tdf_utility/
COPY tdf_api/ /app/

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]