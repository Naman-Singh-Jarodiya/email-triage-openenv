    FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir pydantic openai

ENV HF_TOKEN=""

CMD ["python", "inference.py"]