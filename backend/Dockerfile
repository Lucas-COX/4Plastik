FROM python:3.12

ARG API_KEY

WORKDIR /tmp/app

COPY ./requirements.txt /tmp/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/app/requirements.txt

COPY . /tmp/app

RUN python scripts/database.py
RUN echo $API_KEY | python scripts/create_api_key.py

CMD fastapi run main.py --port 8080
