FROM python:3.9-slim
ENV TZ=Europe/Moscow
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update \
    && apt-get install -y tzdata curl \
    && rm -rf /var/lib/apt/lists/*
COPY bot/requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY bot .
CMD ["python", "bot.py"]
