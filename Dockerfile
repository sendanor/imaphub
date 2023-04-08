FROM python:3.9-slim-buster

ARG IMAP_SERVER=default-server
ARG IMAP_PORT=143
ARG IMAP_USERNAME=default-username
ARG IMAP_PASSWORD=default-password
ARG IMAP_MAILBOX=default-mailbox
ARG HOST=0.0.0.0
ARG PORT=4001

ENV IMAP_SERVER=${IMAP_SERVER}
ENV IMAP_PORT=${IMAP_PORT}
ENV IMAP_USERNAME=${IMAP_USERNAME}
ENV IMAP_PASSWORD=${IMAP_PASSWORD}
ENV IMAP_MAILBOX=${IMAP_MAILBOX}
ENV HOST=${HOST}
ENV PORT=${PORT}

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
