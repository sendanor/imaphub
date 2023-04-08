import unittest
from mailbox import mailbox_parser


class TestMailbox(unittest.TestCase):

    def test_mailbox_parser(self):
        mailbox_list_string = '(\HasNoChildren) "/" INBOX'
        expected_output = {
            'name': 'INBOX',
            'delimiter': '/',
            'flags': ['HasNoChildren'],
            'ref': {
                'mailboxes': '/v1/mailboxes/INBOX/messages'
            }
        }
        self.assertEqual(mailbox_parser(mailbox_list_string), expected_output)

    def test_mailbox_parser_with_no_flags(self):
        mailbox_list_string = '"/" INBOX'
        expected_output = {
            'name': 'INBOX',
            'delimiter': '/',
            'flags': [],
            'ref': {
                'mailboxes': '/v1/mailboxes/INBOX/messages'
            }
        }
        self.assertEqual(mailbox_parser(mailbox_list_string), expected_output)

    def test_mailbox_parser_with_no_flags_2(self):
        mailbox_list_string = '() "/" INBOX'
        expected_output = {
            'name': 'INBOX',
            'delimiter': '/',
            'flags': [],
            'ref': {
                'mailboxes': '/v1/mailboxes/INBOX/messages'
            }
        }
        self.assertEqual(mailbox_parser(mailbox_list_string), expected_output)

    def test_mailbox_parser_with_multiple_flags(self):
        mailbox_list_string = '(\Flagged \Deleted) "/" Important'
        expected_output = {
            'name': 'Important',
            'delimiter': '/',
            'flags': ['Flagged', 'Deleted'],
            'ref': {
                'mailboxes': '/v1/mailboxes/Important/messages'
            }
        }
        self.assertEqual(mailbox_parser(mailbox_list_string), expected_output)


if __name__ == '__main__':
    unittest.main()
