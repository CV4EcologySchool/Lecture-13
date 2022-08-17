# FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04
FROM continuumio/anaconda3:latest

ENV GRADIO_SERVER_PORT 5000

# Install apt packages
RUN set -ex \
 && apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        git \
        htop \
 && rm -rf /var/cache/apt \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./ /code

RUN conda install pip \
 && pip install --no-cache-dir -r requirements.txt

# Port for the web server
EXPOSE 5000

CMD python app.py
