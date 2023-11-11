FROM python:3.11

# Install Pipenv
RUN pip3 install pipenv

ENV PROJECT_DIR /companies
# Set work directory
WORKDIR $PROJECT_DIR

# Copy files to docker image
COPY Pipfile .
COPY Pipfile.lock .
COPY newrelic.ini
COPY . .

RUN pipenv install --deploy --ignore-pipfile

# Expose port for companies microservice
EXPOSE 3002

CMD ["pipenv", "run", "newrelic-admin", "run-program", "python", "main.py"]