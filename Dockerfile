FROM kennethreitz/pipenv as build
ADD . /app
WORKDIR /app
RUN pipenv install \
 && pipenv lock -r > requirements.txt \
 && pipenv run python setup.py bdist_wheel
