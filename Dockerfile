FROM python:3.12.5

ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /usr/src/app

# Copy project files into the container
COPY pyproject.toml /usr/src/app/

# Install Poetry
RUN pip install poetry && \
    poetry install && \
    poetry add --no-cache gunicorn

# Copy the project code into the container
COPY . .
