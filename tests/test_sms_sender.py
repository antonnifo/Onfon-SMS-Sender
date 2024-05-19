import unittest
from unittest.mock import patch, Mock
from sms_sender import send_sms
import os
from dotenv import load_dotenv


try:
    from django.conf import settings
except ImportError:
    pass

load_dotenv()  # Load environment variables from .env file


class TestSendSMS(unittest.TestCase):

    def setUp(self):
        """
        Set up test case with environment or settings variables and mock data.
        """
        # Load variables from environment or settings
        self.api_url = os.getenv(
            'SMS_API_URL', getattr(settings, 'SMS_API_URL', None))
        self.client_id = os.getenv(
            'SMS_CLIENT_ID', getattr(settings, 'SMS_CLIENT_ID', None))
        self.api_key = os.getenv(
            'SMS_API_KEY', getattr(settings, 'SMS_API_KEY', None))
        self.sender_id = os.getenv(
            'SMS_SENDER_ID', getattr(settings, 'SMS_SENDER_ID', None))
        self.recipients = ["254700000001",
                           "254700000002", "254700000003"] #add your number here in format 254 0r 07
        self.message = "Hello, this is a test message from API"

    @patch('sms_sender.utils.requests.post')
    def test_send_sms_single_recipient(self, mock_post):
        """
        Test sending an SMS to a single recipient.
        """
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success", "message": "Message sent"}
        mock_post.return_value = mock_response

        response = send_sms([self.recipients[0]], self.message)

        # Assert the response
        self.assertEqual(response[0]['status'], "success")
        self.assertEqual(response[0]['message'], "Message sent")

        # Verify that the post request was made with the correct data
        expected_payload = {
            "SenderId": self.sender_id,
            "MessageParameters": [
                {"Number": self.recipients[0], "Text": self.message}
            ],
            "ApiKey": self.api_key,
            "ClientId": self.client_id
        }
        mock_post.assert_called_once_with(
            self.api_url,
            data=unittest.mock.ANY,
            headers={'Content-Type': 'application/json'}
        )
        actual_payload = mock_post.call_args[1]['data']
        self.assertEqual(json.loads(actual_payload), expected_payload)

    @patch('sms_sender.utils.requests.post')
    def test_send_sms_multiple_recipients(self, mock_post):
        """
        Test sending an SMS to multiple recipients in batches.
        """
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success", "message": "Messages sent"}
        mock_post.return_value = mock_response

        response = send_sms(self.recipients, self.message)

        # Assert the response
        for res in response:
            self.assertEqual(res['status'], "success")
            self.assertEqual(res['message'], "Messages sent")

        # Verify that the post requests were made with the correct data
        expected_payloads = [
            {
                "SenderId": self.sender_id,
                "MessageParameters": [
                    {"Number": self.recipients[i], "Text": self.message}
                    for i in range(j, min(j + 20, len(self.recipients)))
                ],
                "ApiKey": self.api_key,
                "ClientId": self.client_id
            }
            for j in range(0, len(self.recipients), 20)
        ]
        self.assertEqual(mock_post.call_count, len(expected_payloads))
        for call, expected_payload in zip(mock_post.call_args_list, expected_payloads):
            actual_payload = call[1]['data']
            self.assertEqual(json.loads(actual_payload), expected_payload)

    @patch('sms_sender.utils.requests.post')
    def test_send_sms_api_failure(self, mock_post):
        """
        Test handling of an API failure response.
        """
        # Mock the API response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "status": "error", "message": "Internal server error"}
        mock_post.return_value = mock_response

        response = send_sms([self.recipients[0]], self.message)

        # Assert the response
        self.assertEqual(response[0]['error'],
                         '500 Server Error: None for url: None')


if __name__ == '__main__':
    unittest.main()
