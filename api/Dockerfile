FROM python:3.9

COPY ./Pipfile /code/
WORKDIR /code
RUN pip install pipenv
RUN pipenv lock
RUN pipenv install --system --deploy --ignore-pipfile

WORKDIR /code
ENTRYPOINT ./run.sh
