FROM python:3.14-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

EXPOSE 8000

ENV DEBUG false
ENV SECRET_KEY unsafe

ADD pyproject.toml ./

RUN uv sync

ADD . .

RUN uv run ./manage.py collectstatic --noinput

CMD ["uv", "run", "opentelemetry-instrument", "gunicorn", "-b", "0.0.0.0:8000", "app.wsgi", "--log-file", "-", "--access-logfile", "-", "--error-logfile", "-"]
