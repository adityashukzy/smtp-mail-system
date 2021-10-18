import re
import yaml
import pickle
import socket
import argparse
from rich.table import Table
from rich.console import Console

def email_is_valid(email_ID):
    return bool(re.search("[a-zA-Z0-9](\w|-|\.|_)+@[a-zA-Z]+\.[a-z]", email_ID))

""" Client -> Server_B """
def receive_email_from_client_B():
    HOST = '127.0.0.1'
    PORT = 9999

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sc_sock:
        sc_sock.bind((HOST, PORT))
        sc_sock.listen()
        print("Server is up and listening for connection requests!")

        client_conn, client_addr = sc_sock.accept()
        print(f"Connected with Client at address: {client_addr[0]} and port: {client_addr[1]}")

        # now client will send a token to server, indicating what action it wishes to do:
        while True:
            client_msg = client_conn.recv(1024).decode(encoding="UTF-8")

            if client_msg == "NOOP":
                '''
                COMMAND: Client is testing the connection.
                RESPONSE: '250 OK' denotes connection is good.
                '''
                client_conn.send(b"250 OK")

            elif client_msg == "HELO":
                '''
                COMMAND: Client is asking to initiate an SMTP session conversation.
                RESPONSE: '205 OK' tells client that the SMTP connection is initiated for further communication.
                '''
                client_conn.send(b"250 OK")
            
            elif "MAIL FROM" in client_msg:
                '''
                COMMAND: Client wishes to initiate mail transfer. 'MAIL FROM' is followed by the sender email ID.
                RESPONSE:
                        '250 OK' denotes that email ID has been parsed, validated and stored. Client can continue with further communication.
                        '553' denotes that email ID is not valid.
                '''
                sender_ID = client_msg.split(" ")[2]
                
                if email_is_valid(sender_ID):
                    client_conn.send(b"250 OK")
                    # For debugging purposes:
                    # print(f"Sender ID: {sender_ID}")
                else:
                    sender_ID = None
                    client_conn.send(b"553")
            
            elif "RCPT TO" in client_msg:
                '''
                COMMAND: Client provides recipient/receiver email ID after 'RCPT TO'.
                RESPONSE:
                        '250 OK' denotes that email ID has been parsed, validated and stored. Client can continue with further communication.
                        '553' denotes that email ID is not valid.
                '''
                receiver_ID = client_msg.split(" ")[2]
                
                if email_is_valid(receiver_ID):
                    client_conn.send(b"250 OK")
                    # For debugging purposes:
                    # print(f"Receiver ID: {receiver_ID}")
                else:
                    receiver_ID = None
                    client_conn.send(b"553")
            
            elif client_msg == "DATA":
                '''
                COMMAND: Client wishes to begin sending email content.
                RESPONSE:
                        '354' is an intermediate response denoting that server is ready to receive email content.
                        '250 OK' at the end denotes successful receipt of email.
                        '550 ERROR' at the end denotes email could not be received.
                '''
                client_conn.send(b"354")
                
                exception = False
                try:
                    # Receive email object in pickled format
                    mail_pickle = client_conn.recv(4096)

                    # Unpickle it
                    mail_obj = pickle.loads(mail_pickle)

                    # Store email in internal mailbox (in YAML format)
                    mail = [{'from': mail_obj.sender_ID, 'to': mail_obj.receiver_ID, 'timestamp': mail_obj.timestamp, 'subject': mail_obj.subject, 'body': mail_obj.body}]

                    with open('smtp/group_B/outbox_B.yaml', 'a') as file:
                        document = yaml.dump(mail, file)
                except:
                    # Alert client that email contents could not be received successfully
                    client_conn.send(b"550 ERROR")
                    exception = True
                
                if not exception:
                    client_conn.send(b"250 OK")
            
            elif client_msg == "QUIT":
                '''
                COMMAND: Client has asked to terminate conection between itself and server.
                RESPONSE: '221 BYE' tells client that the connection is being terminated and it can do the same on its side as well.
                '''
                client_conn.send(b"221 BYE")
                break


""" Server_B -> Client """
def access_mailbox_B(email_ID):
    table = Table(show_header=True, header_style='bold magenta')
    table.add_column("From")
    table.add_column("To")
    table.add_column("Time Sent")
    table.add_column("Subject", width=25)
    table.add_column("Body", width=50)
        
    with open('smtp/group_B/inbox_B.yaml', 'r') as file:
        mailbox = yaml.load(file, Loader=yaml.FullLoader)

        if mailbox:
            inboxForGivenID = [mail for mail in mailbox if mail['to'] == email_ID]

            for mail in inboxForGivenID:
                table.add_row(mail['from'], mail['to'], mail['timestamp'], mail['subject'], mail['body'], end_section=True)
        
            console = Console()
            console.print(f"\n[bold magenta]Inbox for {email_ID}![/bold magenta]\n", justify='center')
            console.print(table, justify='center')
        
        else:
            print("No emails in the server mailbox!")


""" Server_B -> Server_A """
def transmit_email_to_server_A():
    """
        Transmission of email from SERVER_B -> SERVER_A.
            - Turns on server B so as to connect with server A and sends all emails collected in the internal mailbox so far.
        NOTES:
            - ss_sock: server-server socket
            - port used: 7777
    """

    HOST = '127.0.0.1'
    PORT = 7777

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss_sock:
        ss_sock.bind((HOST, PORT))
        ss_sock.listen()
        print("Server B is listening and waiting for server A to connect....")

        serverA_conn, serverA_addr = ss_sock.accept()
        print(f"Connected with Server A at address: {serverA_addr[0]} and port: {serverA_addr[1]}")

        # Server B will first transmit all the emails it has in its outbox that need to be sent to Server A
        # Server B will transmit all the emails as one YAML file
        with open('smtp/group_B/outbox_B.yaml', 'rb') as file:
            l = file.read(2048)
            while l:
                serverA_conn.send(bytes(l))
                l = file.read(2048)
    
    print("Email sent to server A successfully!")


""" Server_A -> Server_B """
def receive_email_from_server_A():
    HOST = '127.0.0.1'
    PORT = 5555

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss_sock:
        ss_sock.connect((HOST, PORT))
        
        with open('smtp/group_B/inbox_B.yaml', 'wb') as file:
            while True:
                data = ss_sock.recv(2048).decode()
                if not data:
                    break
                file.write(bytes(data, encoding="UTF-8"))


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description='Run server B in different modes.')

    my_parser.add_argument('Mode',
                            metavar='mode',
                            type=str,
                            help="Type 'fetch' to fetch emails from users in server A. Type 'send' to send email to a user in server A. Type 'inbox' to view your inbox.")
    
    my_parser.add_argument('-y',
                            metavar='--your_email',
                            action='store',
                            help="If you are running server B in inbox mode, please specify your email id so that emails sent to you may be displayed.")

    args = my_parser.parse_args()
    mode = args.Mode
    email_ID = args.y

    console = Console()

    if mode == 'send':
        # turn on server B and have client write and send it 
        receive_email_from_client_B()

        # ask user to turn on server A so email can be transmitted to it
        print("Please turn on Server A now so that email can be transmitted to it!")
        transmit_email_to_server_A()
    
    elif mode == 'fetch':
        # turn on server B to receive any incoming email from server A
        receive_email_from_server_A()
    
    elif mode == 'inbox':
        if not email_ID:
            console.print("\nPlease provide your email id to check your inbox!\n[bold magenta]Example:[/bold magenta] [u][i]python server_B.py inbox -y example@gmail.com[/i][/u]\n")
        else:
            access_mailbox_B(email_ID)
   
    else:
        print("Invalid mode selected!")
