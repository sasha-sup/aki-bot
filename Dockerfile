FROM python:3.6-slim
ENV PYTHONNONBUFFERED 1
COPY . .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
