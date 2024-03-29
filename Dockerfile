FROM python:3.10-alpine3.16

RUN mkdir -p /app
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]