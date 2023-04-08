import os
from flask import Flask, jsonify
import imaplib
import email
import logging
import time

app = Flask(__name__)


@app.route('/')
def get_index():
    return 'ImapHub Ready.'


@app.route('/v1')
def get_v1_index():
    return jsonify({
        'server': 'imaphub',
        'readyStatus': 'READY'
    })


@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f'Unhandled exception: {str(e)}')
    return jsonify({'error': 'An error occurred'}), 500


@app.errorhandler(404)
def handle_404(e):
    return jsonify({'error': 'Not found'}), 404


@app.route('/v1/messages')
def get_messages():
    imap_ssl_enabled = os.environ.get('IMAP_SSL', 'true') == 'true'
    imap_server = os.environ.get('IMAP_SERVER', 'localhost')
    if imap_ssl_enabled:
        default_imap_port = 993
    else:
        default_imap_port = 143
    imap_port = int(os.environ.get('IMAP_PORT', default_imap_port))

    try:
        messages = []

        if imap_ssl_enabled:
            logging.info(f'Connecting to IMAP server {imap_server}:{imap_port} with SSL')
            M = imaplib.IMAP4_SSL(imap_server, imap_port)
        else:
            logging.info(f'Connecting to IMAP server {imap_server}:{imap_port} without SSL')
            M = imaplib.IMAP4(imap_server, imap_port)

        M.login(os.environ.get('IMAP_USERNAME', ''), os.environ.get('IMAP_PASSWORD', ''))

        M.select()

        _, message_ids = M.search(None, 'ALL')
        for message_id in message_ids[0].split():
            _, data = M.fetch(message_id, '(RFC822)')
            message = email.message_from_bytes(data[0][1])
            messages.append({
                'id': message_id.decode(),
                'subject': message['subject'],
                'from': message['from'],
                'to': message['to'],
                'date': message['date'],
                'body': message.get_payload()
            })
        M.close()
        M.logout()

        logging.info(f'Retrieved {len(messages)} messages')
        return jsonify(messages)

    except ConnectionRefusedError as e:
        logging.error(f'Error connecting to IMAP server {imap_server}:{imap_port} (SSL: {imap_ssl_enabled}): {str(e)}')
        return jsonify({'error': 'Could not connect to IMAP server'}), 500

    except imaplib.IMAP4.error as e:
        logging.error(f'Error connecting to IMAP server {imap_server}:{imap_port} (SSL: {imap_ssl_enabled}): {str(e)}')
        return jsonify({'error': 'Could not connect to IMAP server'}), 500


if __name__ == '__main__':
    app.run(debug=True, host=os.environ.get('HOST', '0.0.0.0'), port=int(os.environ.get('PORT', 4001)))
