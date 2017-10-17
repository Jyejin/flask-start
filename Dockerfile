FROM ubuntu:latest
MAINTAINER Juyoung Maeng "philogrammer@gmail.com"

RUN apt-get update -y
RUN apt-get install -y locales python3-pip python3-dev python3-virtualenv fabric \
      libpq-dev libjpeg-dev libxml2-dev libxslt-dev libfreetype6-dev libffi-dev \
      postgresql-client git curl wget
ADD . /flask-start
WORKDIR /flask-start
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["hello.py"]
