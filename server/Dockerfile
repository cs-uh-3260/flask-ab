FROM python:3.10-alpine

WORKDIR /app
COPY . /app

EXPOSE 6969

RUN chmod +x gunicorn_starter.sh

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["sh", "./gunicorn_starter.sh"]