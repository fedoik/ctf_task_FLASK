FROM python:alpine

WORKDIR /app

COPY . /app

RUN apk add --no-cache busybox

RUN pip3 install -r requirements.txt

RUN adduser -D docker

RUN chown -R docker:docker /app

USER docker

EXPOSE 5000

CMD [ "python3", "main.py" ]