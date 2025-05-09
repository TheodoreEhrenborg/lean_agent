FROM ubuntu:22.04

RUN apt-get update && apt-get install -y curl
RUN curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
RUN apt-get install -y fish
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

WORKDIR /code
