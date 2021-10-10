import re
import yaml
from datetime import datetime
from mail import Mail

def emailIsValid(email_ID):
    return bool(re.search("[a-zA-Z0-9](\w|-|\.|_)+@[a-zA-Z]+\.[a-z]", email_ID))

def storeEmailinMailbox_A(mail_obj):
    # organized as a list of emails
    # each email has 5 key-value pairs
    # from, to, timestamp, subject, body
    mail = [{'from': mail_obj.sender_ID, 'to': mail_obj.receiver_ID, 'timestamp': mail_obj.timestamp, 'subject': mail_obj.subject, 'body': mail_obj.body}]

    with open('server_A_mailbox.yaml', 'a') as file:
        document = yaml.dump(mail, file)

if __name__ == "__main__":
    email = Mail("aditya@gmail.com", "shalini@gmail.com", datetime.now(), "Heya", "Hello\nRegards\nAditya")
    storeEmailinMailbox_A(email)

