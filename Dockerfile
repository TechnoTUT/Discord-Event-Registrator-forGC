FROM ghcr.io/astral-sh/uv:debian-slim

ENV TZ=Asia/Tokyo
RUN apt update
RUN apt install ca-certificates -y

COPY . /der/
WORKDIR /der

RUN uv sync

CMD ["uv", "run", "python", "main.py"]
