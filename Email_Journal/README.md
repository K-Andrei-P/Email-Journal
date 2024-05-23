# Email Journaling
#### Description:
My Email Journaling software gives people the opportunity to keep track of their experiences and achievements throughout their weeks. To be able to create this project, I was required to create a custom email address for me to send email invitations and to receive the journals. Sending invitations is done through the method: 
> def send_journal_email(email: str)

This method has the sender email address stored inside it as well as the app password which is used to login to a gmail email through an app. Storing the password in this way is is not secure, so it is advised to store this password as an environment variable. It also contains the subject and the body of the email to be sent, which are stored inside string variables. Which are then stored in another variable with the help of the built-in python library:

> email

An **EmailMessage** object is stored inside the **em** variable. The Email Information is then stored inside there. Logging into the gmail account and sending the email is done through smtp through the built-in python libraries:

> smtplib and ssl

This invitation email is only sent to the email addresses which are stored inside a text file inside the root folder:

> emails.txt

To add emails to the email pool, you need to use the **-n** argument. It is used like this:

> python project.py -n example@email.com

in which *example@email.com* will be added to the email pool.

This software also contains a delete argument to remove email addresses from the email pool: 

> *-d*, followed by the chosen email address 

Receiving the journals are done inside the method:

> def read_emails()

This method uses the built-in python library:

> imaplib

in order to connect to the email server and retreive emails. Unseen messages are then stored inside the variable ***messages***. ***Messages*** is then split and stored inside the list ***emails_ids***. A loop then fetches the message data from each individual email id and stores them inside the ***msgs*** list. Each of the elements in this variable contains a list, which contains: 

> A tuple containing the content data in bytes 

and

> More Byte Code

A following loop loops through each message in ***msgs*** and looks for the tuple stored inside it. The tuple contains two elements:

> Sender Data

and

> Header and Payload Data

which are both stored as bytes. The second Element containing the header and payload is then accessed and stored inside the variable ***my_msg***. An innerloop then looks for the content which is of type *text/plain*. It then calls a function which stores all the relevant information inside a folder inside the root folder:

Function:

> def storing_relevant_info(sender, date, body)

in which ***sender*** is of type ***str*** and ***date*** is of type ***datetime*** and ***body*** is of type ***str***

Folder:

> ./Journals

The Journals folder contains a folder for each individual email address that has sent an email. Inside each of those folder is a folder of the year in which a given journal was written. Each year-folder contains a month folder. The Month folder organises the given journal in weeks of the month. The function *storing_relevant_information* stores the information inside these week-folders as text files.
