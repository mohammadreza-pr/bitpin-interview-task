FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && apt-get clean

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv && pipenv install --system --deploy

COPY . /app/

RUN chmod +x /app/startup.sh

EXPOSE 8000

CMD ["/app/startup.sh"]

