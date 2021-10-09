import re

def emailIsValid(email_ID):
    return bool(re.search("[a-zA-Z0-9](\w|-|\.|_)+@[a-zA-Z]+\.[a-z]", email_ID))

