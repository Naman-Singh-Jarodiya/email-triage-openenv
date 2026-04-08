FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install uv
RUN uv sync

EXPOSE 7860
CMD ["uv", "run", "server"]