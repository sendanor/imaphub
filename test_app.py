import unittest
import os
import json
from app import app

class TestIMAPAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'ImapHub Ready.')

    def test_v1_index(self):
        response = self.app.get('/v1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'server': 'imaphub',
            'readyStatus': 'READY'
        })

    @unittest.skip("Out of test scope for now")
    def test_messages(self):
        os.environ['IMAP_SERVER'] = 'your_imap_server'
        os.environ['IMAP_PORT'] = 'your_imap_port'
        os.environ['IMAP_USERNAME'] = 'your_imap_username'
        os.environ['IMAP_PASSWORD'] = 'your_imap_password'
        os.environ['IMAP_MAILBOX'] = 'your_imap_mailbox'
        response = self.app.get('/v1/messages')
        self.assertEqual(response.status_code, 200)
        messages = json.loads(response.data)
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
