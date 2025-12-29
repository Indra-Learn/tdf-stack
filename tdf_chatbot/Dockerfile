FROM python:3.12-slim

WORKDIR /app

COPY tdf_chatbot/requirements.txt /app/requirements.txt


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

COPY tdf_utility/ /app/tdf_utility/
COPY tdf_chatbot/ /app/

CMD ["streamlit", "run", "--server.port", "8501", "app.py"]
# CMD ["streamlit", "run", "--server.port", "8501", "--server.enableCORS", "false", "app.py"]