FROM mysql:5.6
MAINTAINER Eli Jose "elijose55@hotmail.com"

# Add a database
ENV MYSQL_DATABASE TAREFAS_DB

# Add the content of the sql-scripts/ directory to your image
# All scripts in docker-entrypoint-initdb.d/ are automatically
# executed during container startup
COPY ./sql-scripts/ /docker-entrypoint-initdb.d/
