FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

## Install ubuntu packages
RUN apt-get update
RUN apt-get install -y postgresql postgis
RUN apt-get install -y python3-pip
RUN apt-get install -y libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk
RUN apt-get install -y libxml2-dev libxslt1-dev python-dev
RUN apt-get install -y nodejs npm

## Install pipenv
RUN pip3 install pipenv
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

## Adding Pipfiles & Install dependencies
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --deploy --system

# Set working directory
RUN mkdir -p /dengue-backend
WORKDIR /dengue-backend
ADD . /dengue-backend/

# Frontend
# WORKDIR /dengue/static
# RUN npm install
# RUN npm run typings install
# RUN npm tsc

CMD sh ./run.sh
