import utils
import pickle
import socket
from mail import Mail

HOST = '127.0.0.1'
PORT = 3333

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
    server_sock.bind((HOST, PORT))
    server_sock.listen()

    client_conn, client_addr = server_sock.accept()
    print(f"Connected with Client at address: {client_addr[0]} and port: {client_addr[0]})")
    
    # now client will send a token to server, indicating what action it wishes to do:
    while True:
        client_msg = repr(client_conn.recv(1024))

        if client_msg == "NOOP":
            '''
            COMMAND: Client is testing the connection.
            RESPONSE: '250 OK' denotes connection is good.
            '''
            client_conn.send("250 OK")

        elif client_msg == "HELO":
            '''
            COMMAND: Client is asking to initiate an SMTP session conversation.
            RESPONSE: '205 OK' tells client that the SMTP connection is initiated for further communication.
            '''
            client_conn.send("250 OK")
        
        elif client_msg.contains("MAIL FROM"):
            '''
            COMMAND: Client wishes to initiate mail transfer. 'MAIL FROM' is followed by the sender email ID.
            RESPONSE:
                    '250 OK' denotes that email ID has been parsed, validated and stored. Client can continue with further communication.
                    '553' denotes that email ID is not valid.
            '''
            sender_ID = client_msg.split(" ")[2]
            
            if utils.emailIsValid(sender_ID):
                client_conn.send("250 OK")
            else:
                sender_ID = None
                client_conn.send("553")
        
        elif client_msg.contains("RCPT TO"):
            '''
            COMMAND: Client provides recipient/receiver email ID after 'RCPT TO'.
            RESPONSE:
                    '250 OK' denotes that email ID has been parsed, validated and stored. Client can continue with further communication.
                    '553' denotes that email ID is not valid.
            '''
            receiver_ID = client_msg.split(" ")[2]
            
            if utils.emailIsValid(receiver_ID):
                client_conn.send("250 OK")
            else:
                receiver_ID = None
                client_conn.send("553")
        
        elif client_msg == "DATA":
            '''
            COMMAND: Client wishes to begin sending email content.
            RESPONSE:
                    '354' is an intermediate response denoting that server is ready to receive email content.
                    '250 OK' at the end denotes successful receipt of email.
                    '550 ERROR' at the end denotes email could not be received.
            '''
            client_conn.send("354")
            
            try:
                # Receive email object in pickled format
                email_pickle = client_conn.recv(4096)

                # Unpickle it
                email = pickle.loads(email_pickle)
            except:
                # Alert client that email contents could not be received successfully
                client_conn.send("550 ERROR")
        
        elif client_msg == "QUIT":
            '''
            COMMAND: Client has asked to terminate conection between itself and server.
            RESPONSE: '221 OK' tells client that the connection is being terminated and it can do the same on its side as well.
            '''
            client_conn.send("221 BYE")
            break