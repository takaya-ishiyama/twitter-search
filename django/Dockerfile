FROM python:3.9.10
ENV PYTHONUNBUFFERED 1

WORKDIR /twitteranalytics
COPY . /twitteranalytics/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD sys/fonts-japanese-gothic.ttf /etc/sys/fonts/
