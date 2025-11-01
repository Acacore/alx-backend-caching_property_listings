# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Set the working directory to /drf
# NOTE: all the directives that follow in the Dockerfile will be executed in
# that directory.
WORKDIR /app

# copy project files
COPY requirements.txt /app/ 


# Install system dependencies (needed for psycopg2 etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
        curl \
        && rm -rf /var/lib/apt/lists/*


# Install Python dependencies
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the project
COPY . /app/

# Expose Django port
EXPOSE 8080

# CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
# # CMD ["%%CMD%%"]