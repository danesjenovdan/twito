FROM python:3.9

COPY ./Pipfile /code/
WORKDIR /code
RUN pip install pipenv
RUN pipenv lock
RUN pipenv install --system --deploy --ignore-pipfile

COPY . /code
WORKDIR /code

CMD ['uwsgi', '--http', '0.0.0.0:5000', '--module', 'app:app', '--enable-threads']
