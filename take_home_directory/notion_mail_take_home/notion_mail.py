import os
import sys
from pprint import pprint
from notion_client import Client # type: ignore
from dotenv import load_dotenv # type: ignore
from datetime import datetime
import pytz

# load our relative environment variables
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
PAGE_ID = os.getenv("PAGE_ID")

# ensure our token exists in case the .env file is edited in the future
if NOTION_TOKEN is None:
    print("NOTION_TOKEN not found in .env file.")
    sys.exit(1)

# ensure our page id exists in case the .env file is edited in the future
if PAGE_ID is None:
    print("PAGE_ID not found in .env file.")
    sys.exit(1)

# make a client
notion = Client(auth=NOTION_TOKEN)

# function to send mail to our parent page
def send_mail(sender, recipient, message):
    try:
        # grab current time for a timestamp to be written to the page
        current_time = datetime.utcnow().isoformat()
        notion.pages.create(
            parent={"database_id": PAGE_ID},
            properties={
                "Message": {"title": [{"text": {"content": message}}]},
                "Sender": {"rich_text": [{"text": {"content": sender}}]},
                "Recipient": {"rich_text": [{"text": {"content": recipient}}]},
                "Date": {"date": {"start": current_time}}
            },
        )
        print('Message sent!')
    except Exception as error:
        print('An error occurred:', error)

# function to read all the mail for on recipient
def read_mail(recipient):
    # try a query on our parent page with our page id
    try:
        response = notion.databases.query(
            database_id=PAGE_ID,
            filter={
                "property": "Recipient",
                "rich_text": {"contains": recipient},
            },
        )
        # list of received messages
        results = response.get('results', [])
        if not results:
            print('No messages found.')
        else:
            print(f"Messages ({len(results)}):")
            print()
            for msg in results:
                sender = msg['properties']['Sender']['rich_text'][0]['text']['content']
                message = msg['properties']['Message']['title'][0]['text']['content']
                timestamp = msg['properties']['Date']['date']['start']
                # convert timestamp to pacific time
                utc_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                # regex
                pacific_time = utc_time.astimezone(pytz.timezone('America/Los_Angeles'))
                pretty_timestamp = pacific_time.strftime('%Y-%m-%d %H:%M:%S %Z')
                print(f"ID: {msg['id']}\nfrom: {sender}\non: {pretty_timestamp}\n{message}\n")
        return len(results)
    except Exception as error:
        print('An error occurred:', error)

# this function deletes a message on a particular id
def delete_mail(message_id):
    try:
        notion.pages.update(
            page_id=message_id,
            archived=True,
        )
        print('Message deleted!')
    except Exception as error:
        print('An error occurred:', error)

# this function will delete all received messages for a certain user
def clear_mail(recipient):
    try:
        response = notion.databases.query(
            database_id=PAGE_ID,
            filter={
                "property": "Recipient",
                "rich_text": {"contains": recipient},
            },
        )
        results = response.get('results', [])
        if not results:
            print('No messages found.')
        else:
            for msg in results:
                message_id = msg['id']
                delete_mail(message_id)
            print(f"Cleared all messages for {recipient}")
    except Exception as error:
        print('An error occurred:', error)

# this function will show all the messages between two users for relevant context
def show_relationship(person1, person2):
    try:
        # query for messages where person1 is the sender or recipient
        response1 = notion.databases.query(
            database_id=PAGE_ID,
            filter={
                "or": [
                    {"property": "Sender", "rich_text": {"contains": person1}},
                    {"property": "Recipient", "rich_text": {"contains": person1}}
                ]
            },
        )

        # query for messages where person2 is the sender or recipient
        response2 = notion.databases.query(
            database_id=PAGE_ID,
            filter={
                "or": [
                    {"property": "Sender", "rich_text": {"contains": person2}},
                    {"property": "Recipient", "rich_text": {"contains": person2}}
                ]
            },
        )

        # our message results as lists
        results1 = response1.get('results', [])
        results2 = response2.get('results', [])
        interaction_messages = []

        # iterate our messages and append them to one list
        for msg in results1:
            sender = msg['properties']['Sender']['rich_text'][0]['text']['content']
            recipient = msg['properties']['Recipient']['rich_text'][0]['text']['content']
            if (sender == person1 and recipient == person2) or (sender == person2 and recipient == person1):
                interaction_messages.append(msg)

        for msg in results2:
            sender = msg['properties']['Sender']['rich_text'][0]['text']['content']
            recipient = msg['properties']['Recipient']['rich_text'][0]['text']['content']
            if (sender == person1 and recipient == person2) or (sender == person2 and recipient == person1):
                if msg not in interaction_messages:
                    interaction_messages.append(msg)

        if not interaction_messages:
            print(f"No interactions found between {person1} and {person2}.")
        else:
            # show all of our messages
            print(f"Interactions between {person1} and {person2} ({len(interaction_messages)}):")
            print()
            for msg in reversed(interaction_messages):
                sender = msg['properties']['Sender']['rich_text'][0]['text']['content']
                recipient = msg['properties']['Recipient']['rich_text'][0]['text']['content']
                message = msg['properties']['Message']['title'][0]['text']['content']
                timestamp = msg['properties']['Date']['date']['start']
                # Convert timestamp to pacific Time
                utc_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                pacific_time = utc_time.astimezone(pytz.timezone('America/Los_Angeles'))
                pretty_timestamp = pacific_time.strftime('%Y-%m-%d %H:%M:%S %Z')
                print(f"ID: {msg['id']}\nfrom: {sender} \nto: {recipient}\non: {pretty_timestamp}\n{message}\n")
    except Exception as error:
        print('An error occurred:', error)

# this function is simply for user interaction, which will determine what command is chosen
def prompt_user():
    print("Welcome to NotionMail!")
    while True:
        print("Please select an option:")
        print("- send: Send mail to a user.")
        print("- read: Check a user's mail.")
        print("- delete: Delete a message with its id")
        print("- clear: Clear all messages for a recipient")
        print("- relationship: Show relationship between two users")
        print("- stop: Stop the running program")
        # prompt the user for their input
        action = input('Please select an option (send/read/delete/clear/relationship/stop): ')
        if action == 'send':
            sender = input('Sender: ')
            recipient = input('Recipient: ')
            message = input('Message: ')
            send_mail(sender, recipient, message)
        elif action == 'read':
            recipient = input('Recipient: ')
            read_mail(recipient)
        elif action == 'delete':
            message_id = input('Message ID: ')
            delete_mail(message_id)
        elif action == 'clear':
            recipient = input('Recipient: ')
            clear_mail(recipient)
        elif action == 'relationship':
            person1 = input('Person 1: ')
            person2 = input('Person 2: ')
            show_relationship(person1, person2)
        elif action == 'stop':
            print('Exiting...')
            break
        else:
            # make sure the user doesn't break the CLI in case they choose a wrong option
            print('Invalid option')
        print()

# main function
if __name__ == "__main__":
    prompt_user()
