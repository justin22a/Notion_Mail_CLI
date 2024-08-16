# Notion CLI API Integration for Messaging
Take home assessment programmed by Justin Adam.

## Description of the Program and Improvements

### Description:
- The program is a CLI that allows users to interact with each other through messaging. The messages can be sent (with timestamps), read, deleted, cleared for a users 'inbox', and even show an entire history between two users. All of this information is stored in a database on a Notion page. 

### Improvements and additions:
- A few tests were added to determine if the API was correctly adding and deleting messages.
- A new function called "clear" was added so that a recipient of messages could clear their entire inbox of messages.
- A new function called "relationship" was added to show all the sent and received messages between two people.
- Messages have a new added field which is the message ID, so that they can be identified and deleted if needed.
- A timestamp was added in the database for each message.
- A new function called delete was added so that a user could delete a particular message.

## Installation and Usage

### How to install and run the program:
- Clone the repository locally with `git clone`.
- Install Python if it isn't already installed.
- Navigate to this directory within the sdk notion-sdk-py/take_home_directory/notion_mail_take_home
- Can be ran in an IDE of choice, or from the command line with `python <file_name>.py`, which in this case would be `python notion_mail.py`.
- Then simply interact with the CLI as desired.
- For testing run python test_notion_mail.py
- OPTIONAL: there is a make file in the directory as well so you can do "make run" for the program, and "make test" for running the testing suite.
- NON-GITHUB: If you choose to not use git clone or download from github, the submission will also contain the entire sdk.

### Toubleshooting
- If there are any issues like dependencies or imports, run a command like this "python -m pip install python-dotenv" while will install dependencies depending on version.
- "pip install library" should also work if versioning isn't an issue 
- If a virtual environment is needed, in the local directory run "python -m venv venv" and "source venv/bin/active" (mac) "venv\Scripts\activate" (windows) and lastly "deactivate" when done. 

## References

- https://developers.notion.com/docs/create-a-notion-integration#getting-started
- https://developers.notion.com/reference/intro
- https://developers.notion.com/reference/parent-object
- https://docs.python.org/3/library/unittest.mock.html
- https://www.w3schools.com/python/python_regex.asp
- https://pypi.org/project/python-dotenv/
- https://stackoverflow.com/questions/69851043/node-scripting-in-command-line-for-testing

## Future Improvements

### Potential future improvements:
- The code could use a lot more testing coverage. There should ideally be at least one or two tests for each function/command to handle their implementations and potentially null scenarios.
- There could be a lot more messaging features like some listed below (would assume new columns in the database):
  - Sending one message to multiple people (separately).
  - Group chats with chat IDs that function to send the message to everyone associated with the chat ID.
  - A blocking feature where a user cannot send a message to another for undesired reasons like spam.
- A testing improvement could be not directly writing to the database, as there could be data collisions, especially if the wrong message was somehow deleted (some tests delete a message).
- A history function could also be useful for a user so they can see all messages they have sent.
- A better formatted CLI could be a worthy investment. Unsure of what is best, maybe in a practical world could receive feedback from actual users.
- Better displaying of data through sorting. Although the data may automatically do this, would be smart to test it as such and hardcode values like timestamps.
- Utilize a filter that would work by time, so reading up to a certain time, clearing, and other functionalities.

## Product and Technical Choices

### Product:
- Wanted to have a functionality where the history between two users could be shown. This is important because if there is a constant log in the CLI, it can be messy to keep up with the context of one particular conversation. This could be done with the 'relationship' function showing all relations between two users, which would be similar to reading texts with someone inside a texting app like iMessage.
- Thought that a clear function was necessary so that a user could clear their 'inbox' if it got too messy, or wanted a fresh start. A future implementation improvement would be to clear all conversations with one particular person though.
- A timestamp is a really cool feature for users since they can gain more context about their messages, especially in a scenario where someone asked for a favor but it was yesterday and likely no longer meaningful. Timestamps are great for giving context. I made the timestamps look readable so a user doesn't have to decode what it means (it displays in the CLI).
- Wanted a delete function so that a particular message could be deleted.

### Technical:
- In order to make a clear function easy to implement, a delete function was made so that the clear function has plenty of code reusability. Making delete first was nice since a message could be deleted, but also be reused for other potential functionalities that would benefit from code reuse.
- The messages all have message IDs, so that they can be uniquely identified. This bodes well especially for messages that could be repeated, like one user saying hi 100 times to the same person. Message IDs are also necessary for deleting particular messages.
- I added a few tests that directly interact with the API and function implementations in `notion_mail.py`. This is crucial because code coverage can save potential issues that would arise later on in the development process when making new functions that rely on already tested functions.
