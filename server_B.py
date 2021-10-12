from rich import console
import yaml
import socket
import argparse
from mail import Mail
from rich.table import Table
from rich.console import Console

def receiveEmailFromServer_A():
    HOST = '127.0.0.1'
    PORT = 5555

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss_sock:
        ss_sock.connect((HOST, PORT))
        
        with open('inbox_B.yaml', 'wb') as file:
            while True:
                data = ss_sock.recv(2048).decode()
                if not data:
                    break
                file.write(bytes(data, encoding="UTF-8"))

def accessMailbox(email_ID):
    table = Table(show_header=True, header_style='bold magenta')
    table.add_column("From")
    table.add_column("To")
    table.add_column("Time Sent")
    table.add_column("Subject", width=25)
    table.add_column("Body", width=50)
        
    with open('inbox_B.yaml', 'r') as file:
        mailbox = yaml.load(file, Loader=yaml.FullLoader)

        if mailbox:
            for mail in mailbox:
                email = Mail(mail['from'], mail['to'], mail['timestamp'], mail['subject'], mail['body'])
                table.add_row(email.sender_ID, email.receiver_ID, email.timestamp, email.subject, email.body, end_section=True)
        
            console = Console()
            console.print(table)
        
        else:
            print("No emails in the server mailbox!")

if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description='Run server B in different modes.')

    my_parser.add_argument('Mode',
                            metavar='mode',
                            type=str,
                            help="Type 'fetch' to fetch emails from A. Type 'send' to send emails to A. Type 'inbox' to access the inbox.")
    
    my_parser.add_argument('-y',
                            metavar='--your_email',
                            action='store',
                            help="If you are running server B in inbox mode, please specify your email id so that emails sent to you may be displayed.")

    args = my_parser.parse_args()
    mode = args.Mode
    email_ID = args.y

    console = Console()

    if mode == 'fetch':
        receiveEmailFromServer_A()
    elif mode == 'send':
        # sendEmailToServer_A()
        pass
    elif mode == 'inbox':
        if not email_ID:
            console.print("\nPlease provide your email id to check your inbox!\n[bold magenta]Example:[/bold magenta] [u][i]python server_B.py inbox -y example@gmail.com[/i][/u]\n")
        else:
            console.print(f"\n\n[bold magenta]Inbox for {email_ID}![/bold magenta]\n", justify='left')
            accessMailbox(email_ID)
    else:
        print("Invalid mode selected!")
