FROM python:2.7-slim
ADD . /src
WORKDIR /src
RUN apt-get -qq update
RUN apt-get install -y gcc build-essential
RUN apt-get install -y python-dev
RUN apt-get -y install python-numpy
RUN pip install -r requirements.txt
CMD python -m bot.app
