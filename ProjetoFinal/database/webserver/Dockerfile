FROM python:3.7
MAINTAINER Eli Jose "elijose55@hotmail.com"
RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r requirements.txt
COPY database.py .

EXPOSE 8000
CMD ["python", "/app/database.py"]
