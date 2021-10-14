# smtp-mail-system
A Python implementation of the internal workings of the SMTP and POP3 protocols for email communication.

## Steps to send an email

Say you are in group A and wish to send an email to a recipient in group B:

1. Turn on server A in 'send' mode so that it can first receive an email from a client in group A and then send it to group B's server (i.e. server B). Use the following command.
  
```
python SMTP/group_A/server_A.py send
```

2. Run the SMTP application (app.py). Enter your email ID and construct an email.

```
python app.py
```

3. Once you're done, this email will be sent to server A (which was listening for incoming connections!). Now, we need server A to send this to its corresponding SMTP server in group B: server B! For this, turn on server B in 'fetch' mode so that it can fetch the email that server A wants to send it!

```
python SMTP/group_B/server_B.py fetch
```

4. The email has now reached server B! Now, the recipient of the email can once again run the SMTP application (app.py).

```
python app.py
```

5. After entering their email ID and selecting the "Access inbox" option, the recipient can easily view this email sent to them (along with all the others sent to them before!).

P.S: The same steps will take place but with the A's being swapped with the B's and vice versa!
