FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE $PORT

CMD [ "python", "app.py" ]


