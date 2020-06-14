FROM python:3.7

WORKDIR /app

EXPOSE 8000

ENV DEBUG false
ENV SECRET_KEY unsafe

RUN pip install poetry

ADD pyproject.toml ./
ADD poetry.lock ./

RUN poetry install

ADD . .

RUN poetry run ./manage.py collectstatic --noinput

CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:8000", "app.wsgi", "--log-file", "-"]