import os
import requests
import unittest

class TestIMAPAPI(unittest.TestCase):

    def setUp(self):
        self.api_url = os.environ.get('API_URL', 'http://localhost:4001')

    def test_index(self):
        response = requests.get(f'{self.api_url}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'ImapHub Ready.')

    def test_v1_index(self):
        response = requests.get(f'{self.api_url}/v1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'server': 'imaphub',
            'readyStatus': 'READY'
        })

    def test_messages(self):
        response = requests.get(f'{self.api_url}/v1/messages')
        messages = response.json()
        self.assertIsInstance(messages, list)
        self.assertGreater(len(messages), 0)
        message = messages[0]
        self.assertIn('id', message)
        self.assertIn('subject', message)
        self.assertIn('from', message)
        self.assertIn('to', message)
        self.assertIn('date', message)
        self.assertIn('body', message)

    def test_post_message(self):
        with open('samples/email.eml', 'rb') as f:
            payload = f.read()
        f.close()
        headers = {'Content-Type': 'message/rfc822'}
        response = requests.post(f'{self.api_url}/v1/messages', data=payload, headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'Email created successfully.'})

    def test_mailboxes(self):
        response = requests.get(f'{self.api_url}/v1/mailboxes')
        mailboxes = response.json()
        self.assertIsInstance(mailboxes, list)
        self.assertGreater(len(mailboxes), 0)
        mailbox = mailboxes[0]
        self.assertIn('name', mailbox)
        self.assertIn('flags', mailbox)
        self.assertIn('delimiter', mailbox)
        self.assertIn('ref', mailbox)
        self.assertIn('mailboxes', mailbox['ref'])

    def test_mailbox_messages(self):

        # Create a test mailbox
        requests.post(f'{self.api_url}/v1/messages', json={
            'subject': 'Test Mailbox Creation',
            'from': 'test@example.com',
            'to': 'test@example.com',
            'body': 'This is a test email for creating a mailbox.'
        })

        # Get the list of mailboxes
        response = requests.get(f'{self.api_url}/v1/mailboxes')
        mailboxes = response.json()
        self.assertIsInstance(mailboxes, list)
        self.assertGreater(len(mailboxes), 0)

        # Select a mailbox with messages
        mailbox_name = None
        for mailbox in mailboxes:
            if len(mailbox['flags']) > 0:
                mailbox_name = mailbox['name']
                break
        self.assertIsNotNone(mailbox_name)

        # Get the list of messages for the mailbox
        response = requests.get(f'{self.api_url}/v1/mailboxes/{mailbox_name}/messages')
        messages = response.json()
        self.assertIsInstance(messages, list)
        self.assertGreater(len(messages), 0)
        message = messages[0]
        self.assertIn('id', message)
        self.assertIn('subject', message)
        self.assertIn('from', message)
        self.assertIn('to', message)
        self.assertIn('date', message)
        self.assertIn('body', message)

if __name__ == '__main__':
    unittest.main()
