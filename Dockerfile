FROM ghcr.io/astral-sh/uv:debian-slim

ENV TZ=Asia/Tokyo
RUN apt update
RUN apt install ca-certificates -y

COPY . /usr/src
WORKDIR /usr/src

RUN uv sync

CMD ["uv", "run", "python", "main.py"]
