FROM python:3.8-alpine

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6000

CMD ["python", "./app.py"]