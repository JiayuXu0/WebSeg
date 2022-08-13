FROM python:3.8.13-slim
ARG DEBIAN_FRONTEND=noninteractive
RUN sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list
RUN cat /etc/apt/sources.list
RUN rm -Rf /var/lib/apt/lists/*
RUN apt-get update

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
  && apt-get install -y wget libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1\
  && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /home/jiayuxu/source/requirements.txt
RUN pip3 install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install -r /home/jiayuxu/source/requirements.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN touch "/root/.netrc"

COPY . /home/jiayuxu/source
