from flask import Flask, jsonify
import imaplib
import email

app = Flask(__name__)

@app.route('/emails')
def get_emails():
    imap_server = imaplib.IMAP4_SSL('imap.example.com')
    imap_server.login('username', 'password')
    imap_server.select('inbox')
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
    app.run(debug=True)
