FROM python:3.11

# Install Pipenv
RUN pip3 install pipenv

ENV PROJECT_DIR /assignments
# Set work directory
WORKDIR $PROJECT_DIR

# Add the following line to set PYTHONPATH
ENV PYTHONPATH=$PROJECT_DIR

# Copy files to docker image
COPY Pipfile .
COPY Pipfile.lock .
COPY . .

RUN pipenv install --deploy --ignore-pipfile
ENV NEW_RELIC_LICENSE_KEY=2871e7153e4b28d60f1c6941c6522eedFFFFNRAL
ENV NEW_RELIC_APP_NAME=assignments

# Expose port for users microservice
EXPOSE 3001

CMD ["pipenv", "run", "newrelic-admin", "run-program", "python", "main.py"]
