import os
from flask import Flask, jsonify
import imaplib
import email

app = Flask(__name__)

@app.route('/emails')
def get_emails():
    imap_server = imaplib.IMAP4_SSL(os.environ['IMAP_SERVER'])
    imap_server.login(os.environ['IMAP_USERNAME'], os.environ['IMAP_PASSWORD'])
    imap_server.select(os.environ['IMAP_MAILBOX'])
    _, message_ids = imap_server.search(None, 'ALL')
    messages = []
    for message_id in message_ids[0].split():
        _, data = imap_server.fetch(message_id, '(RFC822)')
        message = email.message_from_bytes(data[0][1])
        messages.append({
            'id': message_id.decode(),
            'subject': message['subject'],
            'from': message['from'],
            'to': message['to'],
            'date': message['date'],
            'body': message.get_payload()
        })
    imap_server.logout()
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True, host=os.environ.get('HOST', 'localhost'), port=int(os.environ.get('PORT', 5000)))

