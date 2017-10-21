FROM ubuntu:latest
MAINTAINER Juyoung Maeng "philogrammer@gmail.com"

RUN apt-get update -y

RUN apt-get install -y locales

RUN locale-gen ko_KR.UTF-8
ENV LANG ko_KR.UTF-8
ENV LANGUAGE ko_KR:ko
ENV LC_ALL ko_KR.UTF-8

RUN apt-get install -y python3-pip python3-dev python3-virtualenv fabric \
      libpq-dev libjpeg-dev libxml2-dev libxslt-dev libfreetype6-dev libffi-dev \
      postgresql-client git curl wget
      
ADD . /flask-start
WORKDIR /flask-start

RUN pip3 install --upgrade pip
RUN pip3 install requests
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["hello.py"]
