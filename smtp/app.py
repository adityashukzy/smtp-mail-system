from group_A import client_A
from group_B import client_B
from rich import print
from rich.console import Console

def main():
    console = Console()
    console.print("\n\n\t\t[bold magenta]SMTP Mail Service[/bold magenta]\n", justify='center')

    console.print("Are you part of group A or group B?\n", justify='center')
    grp = input()
    console.print(f"Welcome to group {grp}!", justify='center')

    console.print("Operations: ", justify='center')
    console.print("1. Send an email", justify='center')
    console.print("2. Access mailbox", justify='center')
    console.print("Select which operation you would like to do (enter 1 or 2):  ", justify='center')
    option = int(input())
    
    if grp == "A":
        if option == 1:
            console.print("\n\t[u]Let's write the email now![/u]\n", justify='center')
            
            # constructing the email with the help of writeEmail function
            email = client_A.write_email()
            # email = Mail('123@gmail.com', '456@hotmail.com', datetime.now(), 'Hey!', "BYE\nBoY")

            # sending the email to the server
            client_A.send_email_to_server_A(email)

            # confirm delivery of email to user
            console.print("Your email has successfully been sent to the destined mailbox in group B!", justify='center')
        
        elif option == 2:
            pass
        
    elif grp == "B":
        pass

    print("\n\n")

if __name__ == "__main__":
    main()