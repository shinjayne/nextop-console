FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
ADD . /src
WORKDIR /src
RUN pip install -r requirements.txt
# RUN export PATH="/code/sqlite:$PATH"
# ADD ./sqlite/sqlite3 /bin
# ADD ./sqlite/sqlite3_analyzer /bin
# ADD ./sqlite/sqldiff /bin
RUN apt-get -y update
RUN apt-get -y upgrade

#RUN apt-get install postgresql postgresql-contrib
#RUN apt-get install -y sqlite3

#RUN apt-get install -y build-essential chrpath libssl-dev libxft-dev
#RUN apt-get install -y libfreetype6 libfreetype6-dev
#RUN apt-get install -y libfontconfig1 libfontconfig1-dev
#RUN apt-get install -y wget
#RUN cd ~
#RUN         export PHANTOM_JS="phantomjs-2.1.1-linux-i686" \
#            && wget https://bitbucket.org/ariya/phantomjs/downloads/$PHANTOM_JS.tar.bz2 \
#            && tar xvjf $PHANTOM_JS.tar.bz2 \
#            && mv $PHANTOM_JS /code \
#            && ln -sf /code/$PHANTOM_JS/bin/phantomjs /bin
