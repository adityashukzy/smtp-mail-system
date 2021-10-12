from rich import print
from mail import Mail
from datetime import datetime
import server_A, server_B, client

def main():
    print("\n\n\t\t[bold magenta]SMTP Mail Service[/bold magenta]\n")

    grp = input("Are you part of group A or group B?\n")
    print(f"Welcome to group {grp}!")

    print("Operations: ")
    print("1. Send an email")
    print("2. Access mailbox")
    option = int(input("Select which operation you would like to do (enter 1 or 2):  "))
    
    if grp == "A":
        if option == 1:
            print("\n\t[u]Let's write the email now![/u]\n")
            
            # constructing the email with the help of writeEmail function
            email = client.writeEmail()
            # email = Mail('123@gmail.com', '456@hotmail.com', datetime.now(), 'Hey!', "BYE\nBoY")

            # sending the email to the server
            client.sendEmailToServer(email)

            # confirm delivery of email to user
            print("Your email has successfully been sent to the destined mailbox in group B!")
        
        elif option == 2:
            pass
        
        elif grp == "B":
            pass

    print("\n\n")

if __name__ == "__main__":
    main()