FROM python:3.9

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip install flask
RUN pip install requests
RUN mkdir -p /var/log/hmc

EXPOSE 8090

CMD ["python","my_flask.py"]
