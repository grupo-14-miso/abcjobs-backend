# Use the official Python image as a base image
FROM python:3.11

# Install Pipenv
RUN pip3 install pipenv

# Set the working directory
WORKDIR /users

# Copy Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile

# Copy the entire project to the working directory
COPY . .

# Expose port for users microservice
EXPOSE 3000

# Set the command to run your application
CMD ["pipenv", "run", "python", "src/main.py"]
