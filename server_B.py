import yaml
import socket
from mail import Mail

def func():
    HOST = '127.0.0.1'
    PORT = 5555

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ss_sock:
        ss_sock.connect((HOST, PORT))
        
        with open('server_B_mailbox.yaml', 'wb') as file:
            while True:
                data = ss_sock.recv(2048).decode()
                print(data)
                if not data: 
                    break
                file.write(bytes(data, encoding="UTF-8"))

def accessMailbox():
    with open('server_B_mailbox.yaml', 'r') as file:
        mailbox = yaml.load(file, Loader=yaml.FullLoader)
        
        for mail in mailbox:
            mail = Mail(mail['from'], mail['to'], mail['timestamp'], mail['subject'], mail['body'])
            mail.display_mail()

if __name__ == "__main__":
    func()

