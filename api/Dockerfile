FROM python:3.9

COPY ./Pipfile /code/
WORKDIR /code
RUN pip install pipenv
RUN pipenv lock
RUN pipenv install --system --deploy --ignore-pipfile

COPY . /code
WORKDIR /code

CMD ['FLASK_ENV=development', 'flask', 'run', '--host=0.0.0.0']
