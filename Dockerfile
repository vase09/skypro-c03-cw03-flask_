FROM python:3.10-slim

# set work directory
WORKDIR /code

# set environment variables
ENV FLASK_APP=run.py
ENV FLASK_DEBUG=1

# install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . .

# run flask
CMD ["sh", "entrypoint.sh"]