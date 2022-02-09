FROM python:3.9

COPY ./Pipfile /api/
WORKDIR /api/
RUN pip install pipenv
RUN pipenv lock
RUN pipenv install --system --deploy --ignore-pipfile

COPY . /api/
