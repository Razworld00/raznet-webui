FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /app/
COPY static/ /app/static/

EXPOSE 8000

CMD ["chainlit", "run", "app.py", "--port", "8000"]