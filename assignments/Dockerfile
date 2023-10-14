FROM python:3.11

# Install Pipenv
RUN pip3 install pipenv

ENV PROJECT_DIR /users
# Set work directory
WORKDIR $PROJECT_DIR

# Add the following line to set PYTHONPATH
ENV PYTHONPATH=$PROJECT_DIR

# Copy files to docker image
COPY Pipfile .
COPY Pipfile.lock .
COPY . .

RUN pipenv install --deploy --ignore-pipfile

# Expose port for users microservice
EXPOSE 3001

CMD ["pipenv", "run", "python", "src/main.py"]
