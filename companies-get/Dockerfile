FROM python:3.11

# Install Pipenv
RUN pip3 install pipenv

ENV PROJECT_DIR /companies-get
# Set work directory
WORKDIR $PROJECT_DIR

# Copy files to docker image
COPY Pipfile .
COPY Pipfile.lock .
COPY newrelic.ini .
COPY . .

RUN pipenv install --deploy --ignore-pipfile
# Install New Relic agent
ENV NEW_RELIC_LICENSE_KEY=2871e7153e4b28d60f1c6941c6522eedFFFFNRAL
ENV NEW_RELIC_APP_NAME=companies-get

# Expose port for companies microservice
EXPOSE 3007

CMD ["pipenv", "run", "newrelic-admin", "run-program", "python", "main.py"]