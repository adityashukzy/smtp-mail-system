

class Mail:
    """
    Class for describing an email message.
    """
    def __init__(self, sender_ID, receiver_ID, timestamp, subject, body):
        self.sender_ID = str(sender_ID)
        self.receiver_ID = str(receiver_ID)
        self.timestamp = str(timestamp)
        self.subject = str(subject)
        self.body = str(body)
    
    def display_mail(self):
        print("\n=================")
        print(f"From: {self.sender_ID}")
        print(f"To: {self.receiver_ID}")
        print(f"Time of sending: {self.timestamp}")
        print(f"Subject: {self.subject}")
        print(f"Body:\n\n{self.body}")
        print("=================\n")

if __name__ == "__main__":
    body = input("Enter email body: \n")
    mail = Mail("adityashukzy@gmail.com", "shalinishukla75@gmail.com", "Enquiring about your wellbeing!", body)
    mail.display_mail()
