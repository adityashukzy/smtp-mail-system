import yaml
import random
from rich import print
from group_A import client_A
from group_A.server_A import access_mailbox_A
from group_B.server_B import access_mailbox_B
from group_B import client_B
from rich.console import Console

def load_clients_list():
    # Load list of clients for groups A and B
    with open("smtp/group_A/group_A_clients.yaml", 'r') as file:
        group_A_clients = yaml.load(file, Loader=yaml.FullLoader)
    
    with open("smtp/group_B/group_B_clients.yaml", 'r') as file:
        group_B_clients = yaml.load(file, Loader=yaml.FullLoader)

    return group_A_clients, group_B_clients

def register(email_ID):
    register = input("You are not registered with our service as yet! Would you like to register yourself? (y/n): ")
    
    if register in ['yes', 'y', "Yes", "Y"]:
        # Randomly assign new user ID to any of group A or B
        assigned_grp = random.choice([1, 2])
        
        if assigned_grp == 1:
            # Add email to group A
            with open("smtp/group_A/group_A_clients.yaml", 'a') as file:
                doc = yaml.dump([email_ID], file)
            
            grp = 'A'
            print("\nGreat! You have been assigned to group A!")
        elif assigned_grp == 2:
            # Add email to group B
            
            with open("smtp/group_B/group_B_clients.yaml", 'a') as file:
                doc = yaml.dump([email_ID], file)
            
            grp = 'B'
            print("\nGreat! You have been assigned to group B!\n")
    else:
        return None

    return grp

def main():
    group_A_clients, group_B_clients = load_clients_list()

    console = Console()
    console.print("\n\n\t\t[bold underline italic magenta]SMTP Mail Service[/bold underline italic magenta]\n")

    email_ID = input("Please enter your email ID: ")
    if email_ID in group_A_clients:
        grp = "A"
    elif email_ID in group_B_clients:
        grp = "B"
    else:
        grp = register(email_ID)
    
    # if None is returned from register(), exit the program
    if not grp:
        print("\nThank you nonetheless! Have a good day!\n")
        exit()
    

    console.print(f"[bold red]Welcome to group {grp}![/bold red]\n")
    
    console.print("You can either... ")
    console.print("1. Send an email")
    console.print("2. Access your inbox")
    option = int(input("Select which operation you would like to do (enter 1 or 2)... "))
    
    # if client is of group A
    if grp == "A":
        if option == 1:
            console.print("\n\t[u]Let's write the email now![/u]\n")
            
            # constructing the email with the help of writeEmail function
            email = client_A.write_email()
            # email = Mail('123@gmail.com', '456@hotmail.com', datetime.now(), 'Hey!', "BYE\nBoY")

            # sending the email to the server
            client_A.send_email_to_server_A(email)

            # confirm delivery of email to user
            console.print("Your email has successfully been sent to the destined mailbox in group B!")
        
        elif option == 2:
            access_mailbox_A(email_ID)

    # if client is of group B
    elif grp == "B":
        if option == 1:
            console.print("\n\t[u]Let's write the email now![/u]\n")
            
            # constructing the email with the help of writeEmail function
            email = client_B.write_email()
            # email = Mail('123@gmail.com', '456@hotmail.com', datetime.now(), 'Hey!', "BYE\nBoY")

            # sending the email to the server
            client_B.send_email_to_server_B(email)

            # confirm delivery of email to user
            console.print("Your email has successfully been sent to the destined mailbox in group A!")

        elif option == 2:
            access_mailbox_B(email_ID)

    print("\n\n")

if __name__ == "__main__":
    main()
