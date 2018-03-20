FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
ADD . /src
WORKDIR /src


# 1. install postgresql-10 in Debian8(jessie)
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main" >> /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt -y update
RUN apt-get install -y postgresql-10 postgresql-contrib libpq-dev

# 2. install python package
RUN pip install -r requirements.txt


