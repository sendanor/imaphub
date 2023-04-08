import re
import urllib.parse

def mailbox_parser(mailbox_list_string):

    match = re.match(r'\((.*?)\) "(.*?)" (.*)', mailbox_list_string)
    if match:
        flags = match.group(1).split(' ') if match.group(1) else []
        delimiter = match.group(2)
        mailbox_name = match.group(3)
    else:
        match = re.match(r'"(.*?)" (.*)', mailbox_list_string)
        flags = []
        delimiter = match.group(1)
        mailbox_name = match.group(2)

    flags = [flag[1:] if flag.startswith('\\') else flag for flag in flags]

    return {
        'name': mailbox_name,
        'delimiter': delimiter,
        'flags': flags,
        'ref': {
            'mailboxes': f'/v1/mailboxes/{urllib.parse.quote(mailbox_name)}/messages'
        }
    }

