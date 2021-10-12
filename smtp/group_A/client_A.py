import re
import pickle
import socket
from datetime import datetime
from mail import Mail

def email_is_valid(email_ID):
    return bool(re.search("[a-zA-Z0-9](\w|-|\.|_)+@[a-zA-Z]+\.[a-z]", email_ID))

HOST = '127.0.0.1'
PORT = 3333

"""
    PART I: Assembling of email to be sent
"""

def write_email():
    """
    Form the email message including information on sender & recipient ID's, subject and body.
    Returns: Mail object instantiated with user-inputted values.
    """
    while True:
        client_email_id = input("From (your email ID): ")
        if email_is_valid(client_email_id):
            break

    while True:
        receiver_email_ID = input("To (recipient email ID): ")
        if email_is_valid(receiver_email_ID):
            break

    subject = input("Subject: ")
    print("Body: \n")
    body = "\n".join(iter(input, ''))
    mail = Mail(client_email_id, receiver_email_ID, datetime.now(), subject, body)

    return mail


"""
    PART II: Transmission of email from Client -> Server_A
"""

def send_email_to_server_A(email):
    """
    Send the constructed email to server A.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
        client_sock.connect((HOST, PORT))

        # Send 'NOOP' to test connection
        try:
            client_sock.send(b'NOOP')
            server_resp = client_sock.recv(1024).decode(encoding="UTF-8")
        except:
            print("Error connecting to server A!")

        # Send 'HELO' to initiate SMTP session conversation.
        try:
            client_sock.send(b'HELO')
            server_resp = client_sock.recv(1024).decode(encoding="UTF-8")

            if server_resp == "250 OK":
                print("SMTP session ready!")
        except:
            print("Error initiating SMTP session with server A!")

        # Send 'MAIL FROM addr@example.com' to initiate mail transfer to server and indicate sender ID.
        try:
            client_sock.send(bytes("MAIL FROM " + email.sender_ID, encoding="UTF-8"))
            server_resp = client_sock.recv(1024).decode(encoding="UTF-8")

            if server_resp == "250 OK":
                print("Sender email ID validated!")
            elif server_resp == "553":
                print("Error: Email ID is invalid!")
        except:
            print("Error initiating mail transfer with server A!")
        
        # Send 'RCPT TO addr@example.com' to indicate receiver ID.
        try:
            client_sock.send(bytes("RCPT TO " + email.receiver_ID, encoding="UTF-8"))
            server_resp = client_sock.recv(1024).decode(encoding="UTF-8")

            if server_resp == "250 OK":
                print("Receiver email ID validated!")
            elif server_resp == "553":
                print("Error: Email ID is invalid!")

        except:
            print("Error initiating SMTP session with server A!")
        
        # Send 'DATA' to indicate incoming transmission of email body.
        try:
            client_sock.send(b'DATA')
            server_resp = client_sock.recv(1024).decode(encoding="UTF-8")

            if server_resp == "354":
                # continue sending email body object as a pickle
                client_sock.send(pickle.dumps(email))
                server_resp = client_sock.recv(1024).decode(encoding="UTF-8")
                
                if server_resp == "250 OK":
                    print("Email body transmitted to server successfully!")
                elif server_resp == "550 ERROR":
                    print("Error: email body could not be received by server A!")

        except:
            print("Error transmitting email content to server A!")
        
        # Send 'QUIT' to initiate termination of connection
        try:
            client_sock.send(b'QUIT')
            server_resp = client_sock.recv(1024).decode(encoding="UTF-8")

            if server_resp == "221 BYE":
                print("Email successfully sent to server A!")
        except:
            print("Error terminating SMTP connection with server A!")
        
        print("\nEnd of Program!")

if __name__ == "__main__":
    email = Mail("aditya@gmail.com", "shalini@gmail.com", datetime.now(), "Heya", "Dear Adi,\nI love you.\nRegards,\nAditya")
    send_email_to_server_A(email)
