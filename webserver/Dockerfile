FROM python:3.7
MAINTAINER Eli Jose "elijose55@hotmail.com"
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt
COPY webserver.py .

EXPOSE 5000
CMD ["python", "/app/webserver.py"]
