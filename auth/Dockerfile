FROM python:3.4

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY src/requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src /usr/src/app
CMD python src/main.py
