FROM python:3.9

COPY ./Pipfile /api/
WORKDIR /api/
RUN pip install pipenv
RUN pipenv lock
RUN pipenv install --system --deploy --ignore-pipfile

# install twint
# this is done with pip, because the --system
# flag in pipenv can't be used on single dependencies
RUN pip install git+https://github.com/twintproject/twint.git#egg=twint

COPY . /api/

# CMD ['uwsgi', '--http', '0.0.0.0:5000', '--module', 'app:app', '--enable-threads']
ENTRYPOINT ./run.sh
