import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import notion_mail  


class TestNotionMailAddMessage(unittest.TestCase):
    @patch('notion_mail.notion.databases.query')
    @patch('notion_mail.notion.pages.create')
    @patch('notion_mail.notion.pages.update')
    def test_add_message_increases_count(self, mock_update, mock_create, mock_query):
        # Mock the initial query response to simulate existing messages
        initial_response = {
            'results': [
                {
                    'id': 'message_1',
                    'properties': {
                        'Sender': {'rich_text': [{'text': {'content': 'sender1@example.com'}}]},
                        'Recipient': {'rich_text': [{'text': {'content': 'recipient@example.com'}}]},
                        'Message': {'title': [{'text': {'content': 'Hello, this is a test message.'}}]},
                        'Date': {'date': {'start': datetime.utcnow().isoformat()}}
                    }
                }
            ]
        }
        mock_query.return_value = initial_response

        recipient = 'recipient@example.com'

        # get message count for a recipient
        initial_message_count = notion_mail.read_mail(recipient)
        self.assertEqual(initial_message_count, len(initial_response['results']))

        # mock the create method to simulate adding a new message
        mock_create.return_value = None

        # send a new message to test
        notion_mail.send_mail('sender2@example.com', recipient, 'This is another test message.')

        # query the response
        updated_response = {
            'results': initial_response['results'] + [
                {
                    'id': 'message_2',
                    'properties': {
                        'Sender': {'rich_text': [{'text': {'content': 'sender2@example.com'}}]},
                        'Recipient': {'rich_text': [{'text': {'content': recipient}}]},
                        'Message': {'title': [{'text': {'content': 'This is another test message.'}}]},
                        'Date': {'date': {'start': datetime.utcnow().isoformat()}}
                    }
                }
            ]
        }
        mock_query.return_value = updated_response

        # retrieve a new updated message count
        updated_message_count = notion_mail.read_mail(recipient)
        self.assertEqual(updated_message_count, len(updated_response['results']))

        # make sure that after one new message the total count increases by 1
        self.assertEqual(updated_message_count, initial_message_count + 1)

        # moch the create method again
        mock_update.return_value = None

        # delete the message to keep the database clean of testing data
        notion_mail.delete_mail('message_2')

        # mock the query response to simulate the list of messages after deletion
        final_response = initial_response  
        mock_query.return_value = final_response

        # get the final message count
        final_message_count = notion_mail.read_mail(recipient)
        self.assertEqual(final_message_count, len(final_response['results']))

        # make sure the count is back to what it initially was after deleting a test message
        self.assertEqual(final_message_count, initial_message_count)


class TestNotionMailClearMessages(unittest.TestCase):
    @patch('notion_mail.notion.databases.query')
    @patch('notion_mail.notion.pages.create')
    @patch('notion_mail.notion.pages.update')
    def test_clear_messages(self, mock_update, mock_create, mock_query):
        recipient = 'recipient@example.com'

        # mock the initial query response to simulate no existing messages
        initial_response = {'results': []}
        mock_query.return_value = initial_response

        # add two messages to ensure the clear function handles deleting more than one message
        notion_mail.send_mail('sender1@example.com', recipient, 'Message 1')
        notion_mail.send_mail('sender2@example.com', recipient, 'Message 2')

        # mock the query response to simulate the two new messages
        new_response = {
            'results': [
                {
                    'id': 'message_1',
                    'properties': {
                        'Sender': {'rich_text': [{'text': {'content': 'sender1@example.com'}}]},
                        'Recipient': {'rich_text': [{'text': {'content': recipient}}]},
                        'Message': {'title': [{'text': {'content': 'Message 1'}}]},
                        'Date': {'date': {'start': datetime.utcnow().isoformat()}}
                    }
                },
                {
                    'id': 'message_2',
                    'properties': {
                        'Sender': {'rich_text': [{'text': {'content': 'sender2@example.com'}}]},
                        'Recipient': {'rich_text': [{'text': {'content': recipient}}]},
                        'Message': {'title': [{'text': {'content': 'Message 2'}}]},
                        'Date': {'date': {'start': datetime.utcnow().isoformat()}}
                    }
                }
            ]
        }
        mock_query.return_value = new_response

        # retrieve the message count after adding messages
        message_count = notion_mail.read_mail(recipient)
        self.assertEqual(message_count, len(new_response['results']))

        # clear all messages for the recipient
        notion_mail.clear_mail(recipient)

        # mock the query response to simulate no messages after clearing
        empty_response = {'results': []}
        mock_query.return_value = empty_response

        # retrieve the message count after clearing messages
        cleared_message_count = notion_mail.read_mail(recipient)
        self.assertEqual(cleared_message_count, len(empty_response['results']))

        # ensure the message count is zero
        self.assertEqual(cleared_message_count, 0)

if __name__ == '__main__':
    unittest.main()
