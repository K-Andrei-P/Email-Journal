from email.message import EmailMessage
import ssl
import smtplib
import argparse
import sys
import imaplib
import email
import os
from email.utils import parseaddr
from email.utils import parsedate_to_datetime
import re
import shutil

#TODO:

def main():

    emails = set()
    # Put all Email in the Emails Set
    with open("./emails.txt") as file:
        lines = file.readlines()
        for line in lines:
            email = line.strip()
            if email:
                emails.add(email)

    if len(sys.argv) == 1:
        for email in emails:
            print(f"Email sent to {email}")
            send_journal_email(email.strip())

    else:
        parser = argparse.ArgumentParser(description= "Adding and Deleting Email addresses")
        parser.add_argument("-n", help="Add new Email to Email Pool")
        parser.add_argument("-d", help="Delete Email from Email Pool")
        parser.add_argument("-l", help="List all Emails", action="store_true")
        parser.add_argument("-r", help="Reading all Emails from Unread Inbox", action="store_true")
        args = parser.parse_args()

        # Applying Arguments
        if args.n is not None:
            try:
                emails.add(args.n)
                os.mkdir(f"./Journals/{args.n}")
            except ValueError:
                print("Email already exists")
            except FileNotFoundError:
                os.mkdir("./Journals")
                os.mkdir(f"./Journals/{args.n}")
        elif args.d is not None:
            try:
                emails.remove(args.d)
                delete_journal(args.d)
            except KeyError:
                print("Email is not in Email pool")
            else:
                print("Email Deleted")
        elif args.l:
            for email in emails:
                print(email)
        elif args.r:
            print("Reading...")
            read_emails()

        # Write all Emails in emails.txt
        open("./emails.txt", "w").close()
        with open("./emails.txt", "a") as file:
            for email in emails:
                file.write(f"{email}\n")

    return True



def send_journal_email(email: str):
    email_sender = "andrei.cs50p.finalproject@gmail.com"
    email_password = "gaykyrodoejmdubn"

    subject = "Your Journal"
    body = """
    Hey, What's Up!!

    It's that time again, to write Your Journal of the Day!!
    Just write your Journal in a reply to this Email in this Format:

    How Am I Feeling:

    What Have I Achieved Today:

    What Are My Goals:

    Other:

    At the End of the Week, you will receive a summary of all your Journals throughout the week.

    Thank you!
    """

    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email
    em["Subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email, em.as_string())
        return True


# Test exit code 0
def read_emails():
    email_address = "andrei.cs50p.finalproject@gmail.com"
    password = "gaykyrodoejmdubn"

    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(email_address, password)
    print("Logged in")

    mail.select("Inbox")

    _, messages = mail.search(None, "(UNSEEN)")
    
    # Email Ids
    email_ids = messages[0].split()
    print("Ids saved")

    # Contains the list from messages from ids
    # Each List Element contains a tuple and something else
    msgs = []

    for email_id in email_ids:
        _, msg_data = mail.fetch(email_id, "(RFC822)")
        msgs.append(msg_data)
        mail.store(email_id, '-FLAGS', '\\Seen')

    # NOTE: Message contains header and payload
        
    # Go through each list inside msgs
    for msg in msgs:
        # Go through listpart inside list
        for response_part in msg:
            # Check if the resonsepart is a tuple
            # tuple is the size of 2, second element is the important one
            if type(response_part) is tuple:
                # accessing 2nd element
                my_msg = email.message_from_bytes((response_part[1]))
                # My_msg contains header and payload, we need to access payload
                for part in my_msg.walk():
                    if part.get_content_type() == "text/plain":
                        # part.get_payload(decode=True).decode("utf-8") returns a string
                        storing_relevant_info(my_msg["from"], parsedate_to_datetime(my_msg["date"]), part.get_payload(decode=True).decode("utf-8"))

    return True

# Test with different Stringed Emails
def storing_relevant_info(sender, date, body):
    dir_name = "./Journals"
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    
    # Can be put into a seperate Function
    name, email_address = parseaddr(sender)
    string_date = f"{date.year}-{date.month}-{date.day}"

    path = f"{dir_name}/{email_address}"

    # checks if email address has directory
    # ./Journals/email@gmail.com
    if not os.path.isdir(path):
        os.mkdir(path)

    # checks if year directory is in email address directory
    # ./Journals/email@gmail.com/2024
    if not os.path.isdir(f"{path}/{date.year}"):
        os.mkdir(f"{path}/{date.year}")
    path = f"{path}/{date.year}"
    # checks if month directory is in year directory
    # ./Journals/email@gmail.com/2024/February
    if not os.path.isdir(f"{path}/{date.strftime('%B')}"):
        os.mkdir(f"{path}/{date.strftime('%B')}")
    path = f"{path}/{date.strftime('%B')}"
    # checks which week of month
    # ./Journals/email@gmail.com/2024/February/Week-1
    if not os.path.isdir(f"{path}/{determine_week(date.day)}"):
        os.mkdir(f"{path}/{determine_week(date.day)}")
    path = f"{path}/{determine_week(date.day)}"
    # Writing file inside directory
    # Full directory example: /example@gmail.com/2014/01/Week1/
    open(f"{path}/{string_date}.txt", "w").close()
    with open(f"{path}/{string_date}.txt", "a", encoding="utf-8") as file:
        file.write(name)
        file.write("\n" * 3)
        body.replace(">", "").strip()

        try:
            lines = body.split("\n")
            index = lines.index("________________________________\r")
        except ValueError:
            pass
        else:
            body = '\n'.join(lines[:index])
        
        try:
            lines = body.split("\n")
            index = lines.index("From: andrei.cs50p.finalproject@gmail.com<mailto:andrei.cs50p.finalproject@gmail.com>\r")
        except ValueError:
            pass
        else:
            body = '\n'.join(lines[:index])

        match = re.search(r"On\s\w{3},\s\w{3}\s\d{1,2},\s\d{4}\sat\s\d{1,2}:\d{2}\s[AM|PM].*", body)

        if match:
            start_index = match.start()
            body = body[:start_index].strip()

        file.write(body)

    print(f"Finished Writing: {email_address}")
    return True

def determine_week(day):
    week = 0

    if day <= 7:
        week = 1
    elif day <= 15:
        week = 2
    elif day <= 23:
        week = 3
    elif day <= 31:
        week = 4
    else:
        return False

    return f"Week-{week}"

def delete_journal(email):
    shutil.rmtree(f"./Journals/{email}")

if __name__ == "__main__":
    main()