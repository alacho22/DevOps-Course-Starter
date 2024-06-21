FROM python:3.12 as base

WORKDIR /app
ENV FLASK_APP=todo_app/app
EXPOSE 5000
RUN pip install poetry==1.8.3
COPY poetry.lock poetry.toml pyproject.toml ./

FROM base as production

ENV FLASK_ENV=production
ENV FLASK_DEBUG=false
RUN poetry install --no-interaction --no-root --without dev
COPY todo_app ./todo_app
ENTRYPOINT [ "poetry", "run", "flask", "run", "--host=0.0.0.0" ]

FROM base as development

ENV FLASK_ENV=development
ENV FLASK_DEBUG=true
RUN poetry install --no-interaction --no-root
ENTRYPOINT [ "poetry", "run", "flask", "run", "--host=0.0.0.0" ]