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

if __name__ == '__main__':
    unittest.main()
