# FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04
FROM continuumio/anaconda3:latest

ENV GRADIO_SERVER_NAME=0.0.0.0

ENV GRADIO_SERVER_PORT=7860

# Install apt packages
RUN set -ex \
 && apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        git \
        vim \
        htop \
 && rm -rf /var/cache/apt \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY ./ /code

RUN conda install pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install numpy --upgrade \
 && conda install pytorch torchvision cpuonly -c pytorch-nightly

CMD python app.py
