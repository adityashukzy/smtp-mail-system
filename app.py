from mail import Mail
from datetime import datetime
import server_A, server_B, client

def main():
    print("\n\n~~~~~~~~~ Welcome to the SMTP Mail Service ~~~~~~~~~\n\n")

    grp = input("Are you part of group A or group B? (type A for group A, B for group B)")
    
    if grp == "A":
        print("Welcome to group A!")

        print("Operations: ")
        print("1. Send an email")
        print("2. Access mailbox")
        option = int(input("Select which operation you would like to do (enter 1 or 2):  "))

        if option == 1:
            print("\nLet's write the email now!\n")
            
            # constructing the email with the help of writeEmail function
            # email = client.writeEmail()
            email = Mail('123@gmail.com', '456@hotmail.com', datetime.now(), 'Hey!', "BYE\nBoY")

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