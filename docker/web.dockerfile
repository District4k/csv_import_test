FROM python:3.11

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]

