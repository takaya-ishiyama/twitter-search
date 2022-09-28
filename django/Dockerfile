FROM python:3.9.10
ENV PYTHONUNBUFFERED 1

WORKDIR /twitteranalytics
COPY requirements.txt /twitteranalytics/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./etc/mecabrc /etc/
COPY . /twitteranalytics/
ADD sys/fonts-japanese-gothic.ttf /etc/sys/fonts/

