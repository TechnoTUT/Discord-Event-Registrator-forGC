FROM ghcr.io/astral-sh/uv:debian-slim

RUN apt update
RUN apt install ca-certificates -y
