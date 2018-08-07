FROM python:3.7.0-alpine3.8

WORKDIR /app

EXPOSE 8000

ENV DEBUG false
ENV SECRET_KEY unsafe

RUN pip install pipenv && \
    apk add postgresql-dev gcc python3-dev musl-dev

ADD Pipfile* ./

RUN pipenv install

ADD . .

RUN pipenv run ./manage.py collectstatic --noinput

CMD ["pipenv", "run", "gunicorn", "-b", "0.0.0.0:8000", "app.wsgi", "--log-file", "-"]