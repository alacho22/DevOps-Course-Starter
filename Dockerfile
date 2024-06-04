FROM python:3.12

RUN pip install poetry==1.8.3

COPY poetry.lock poetry.toml pyproject.toml ./
RUN poetry install --without dev

COPY todo_app ./todo_app

ENV FLASK_APP=todo_app/app

EXPOSE 5000
ENTRYPOINT [ "poetry", "run", "flask", "run", "--host=0.0.0.0" ]