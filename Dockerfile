FROM python:3.10-slim

WORKDIR /app
COPY . /app

RUN pip install uv
RUN uv sync

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 7860
CMD ["server"]