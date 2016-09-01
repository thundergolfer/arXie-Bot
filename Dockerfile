FROM python:2.7-slim
ADD . /src
WORKDIR /src
RUN apt-get -qq update
RUN apt-get -y install python-numpy
RUN pip install -r requirements.txt
CMD python ./bot/app.py
