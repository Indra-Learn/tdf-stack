FROM python:3.12-slim

WORKDIR /app

COPY quant_wealth_partner/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8502

COPY quant_wealth_partner/ /app/

CMD ["streamlit", "run", "--server.port", "8502", "streamlit_app.py"]
# CMD ["streamlit", "run", "--server.port", "8502", "--server.enableCORS", "false", "app.py"]