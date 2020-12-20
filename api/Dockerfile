FROM python:3.9
ADD . /code
WORKDIR /code
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
CMD python app.py
