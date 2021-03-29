FROM python:3.9.2

#WORKDIR /usr/src/django_fantasia

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY django_fantasia .
COPY fantasia .
COPY media .
COPY templates .
COPY manage.py .

EXPOSE 8000

CMD ['gunicorn --bind 0.0.0.0:8000 django_fantasia.wsgi:application']