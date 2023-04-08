#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2023 Jaakko Heusala <jheusala@iki.fi>. All rights reserved.

import os
from flask import Flask, jsonify, request
import imaplib
import email
import logging
from email.message import EmailMessage
from mailbox import mailbox_parser

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

IMAP_SSL_ENABLED = os.environ.get('IMAP_SSL', 'true') == 'true'
IMAP_SERVER = os.environ.get('IMAP_SERVER', 'localhost')
if IMAP_SSL_ENABLED:
    DEFAULT_IMAP_PORT = 993
else:
    DEFAULT_IMAP_PORT = 143
IMAP_PORT = int(os.environ.get('IMAP_PORT', DEFAULT_IMAP_PORT))
IMAP_USERNAME = os.environ.get('IMAP_USERNAME', '')
IMAP_PASSWORD = os.environ.get('IMAP_PASSWORD', '')
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 4001))


def connect_to_imap_server():
    if IMAP_SSL_ENABLED:
        logging.info(f'Connecting to IMAP server {IMAP_SERVER}:{IMAP_PORT} with SSL')
        M = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    else:
        logging.info(f'Connecting to IMAP server {IMAP_SERVER}:{IMAP_PORT} without SSL')
        M = imaplib.IMAP4(IMAP_SERVER, IMAP_PORT)
    M.login(IMAP_USERNAME, IMAP_PASSWORD)
    return M


def disconnect_from_imap_server(M):
    M.close()
    M.logout()


def build_message(message_bytes: bytes) -> dict:
    message = email.message_from_bytes(message_bytes)
    return {
        'subject': message['subject'],
        'from': message['from'],
        'to': message['to'],
        'date': message['date'],
        'body': message.get_payload()
    }

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f'Unhandled exception: {str(e)}')
    return jsonify({'error': 'An error occurred'}), 500


@app.errorhandler(404)
def handle_404(e):
    return jsonify({'error': 'Not found'}), 404


@app.route('/')
def get_index():
    return 'ImapHub Ready.'


@app.route('/v1')
def get_v1_index():
    return jsonify({
        'server': 'imaphub',
        'readyStatus': 'READY'
    })

@app.route('/v1/messages', methods=['POST'])
def create_message():

    content_type = request.headers.get('Content-Type')

    if content_type == "application/json":
        msg = EmailMessage()
        msg.set_content(request.json.get('body', ''))
        msg['Subject'] = request.json.get('subject', '')
        msg['From'] = request.json.get('from', '')
        msg['To'] = request.json.get('to', '')
    elif content_type == "message/rfc822":
        msg = email.message_from_bytes(request.data)
    else:
        return jsonify({'error': 'Unsupported media type'}), 415

    try:
        M = connect_to_imap_server()
        try:
            M.select()
            M.append('INBOX', None, None, msg.as_bytes())
            return jsonify({'message': 'Email created successfully.'}), 201
        finally:
            disconnect_from_imap_server(M)

    except ConnectionRefusedError as e:
        logging.error(f'Error connecting to IMAP server {IMAP_SERVER}:{IMAP_PORT} (SSL: {IMAP_SSL_ENABLED}): {str(e)}')
        return jsonify({'error': 'Could not connect to IMAP server'}), 500

    except imaplib.IMAP4.error as e:
        logging.error(f'Error connecting to IMAP server {IMAP_SERVER}:{IMAP_PORT} (SSL: {IMAP_SSL_ENABLED}): {str(e)}')
        return jsonify({'error': 'Could not connect to IMAP server'}), 500


@app.route('/v1/messages')
def get_messages():

    try:
        messages = []

        M = connect_to_imap_server()
        try:
            M.select()
            _, message_ids = M.search(None, 'ALL')
            for message_id in message_ids[0].split():
                _, data = M.fetch(message_id, '(RFC822)')
                message = build_message(data[0][1])
                messages.append({
                    'id': message_id.decode(),
                    **message
                })
        finally:
            disconnect_from_imap_server(M)

        logging.info(f'Retrieved {len(messages)} messages')
        return jsonify(messages)

    except ConnectionRefusedError as e:
        logging.error(f'Error connecting to IMAP server {IMAP_SERVER}:{IMAP_PORT} (SSL: {IMAP_SSL_ENABLED}): {str(e)}')
        return jsonify({'error': 'Could not connect to IMAP server'}), 500

    except imaplib.IMAP4.error as e:
        logging.error(f'Error connecting to IMAP server {IMAP_SERVER}:{IMAP_PORT} (SSL: {IMAP_SSL_ENABLED}): {str(e)}')
        return jsonify({'error': 'Could not connect to IMAP server'}), 500


@app.route('/v1/mailboxes')
def get_mailboxes():
    try:
        M = connect_to_imap_server()
        try:
            M.select()
            _, mailboxes = M.list()
        finally:
            disconnect_from_imap_server(M)

        mailboxes_list = []
        for mailbox in mailboxes:
            decoded = mailbox.decode()
            logging.debug(f'Retrieved mailbox: {decoded}')
            mailboxes_list.append(mailbox_parser(decoded))

        return jsonify(mailboxes_list)

    except ConnectionRefusedError as e:
        logging.error(f'Error connecting to IMAP server {IMAP_SERVER}:{IMAP_PORT} (SSL: {IMAP_SSL_ENABLED}): {str(e)}')
        return jsonify({'error': 'Could not connect to IMAP server'}), 500

    except imaplib.IMAP4.error as e:
        logging.error(f'Error connecting to IMAP server {IMAP_SERVER}:{IMAP_PORT} (SSL: {IMAP_SSL_ENABLED}): {str(e)}')
        return jsonify({'error': 'Could not connect to IMAP server'}), 500

@app.route('/v1/mailboxes/<name>/messages')
def get_mailbox_messages(name):
    try:
        M = connect_to_imap_server()
        try:
            M.select(name)
            _, message_ids = M.search(None, 'ALL')
            messages = []
            for message_id in message_ids[0].split():
                _, data = M.fetch(message_id, '(RFC822)')
                message = build_message(data[0][1])
                messages.append({
                    'id': message_id.decode(),
                    **message
                })
        finally:
            disconnect_from_imap_server(M)

        return jsonify(messages)

    except ConnectionRefusedError as e:
        logging.error(f'Error connecting to IMAP server {IMAP_SERVER}:{IMAP_PORT} (SSL: {IMAP_SSL_ENABLED}): {str(e)}')
        return jsonify({'error': 'Could not connect to IMAP server'}), 500

    except imaplib.IMAP4.error as e:
        logging.error(f'Error connecting to IMAP server {IMAP_SERVER}:{IMAP_PORT} (SSL: {IMAP_SSL_ENABLED}): {str(e)}')
        return jsonify({'error': 'Could not connect to IMAP server'}), 500


if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
