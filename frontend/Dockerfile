FROM python:3.10-alpine

COPY ../ .

EXPOSE 8000

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x gunicorn_starter.sh

ENTRYPOINT ["sh", "./gunicorn_starter.sh"]