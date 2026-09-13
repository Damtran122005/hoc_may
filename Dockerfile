FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 3000

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:3000", "--workers", "1"]
