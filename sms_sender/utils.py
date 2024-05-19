import json
import requests
import time
from dotenv import load_dotenv
import os

try:
    from django.conf import settings
except ImportError:
    pass

load_dotenv()  # Load environment variables from .env file


def send_sms(recipients, message):
    """
    Sends SMS messages to a list of recipients using the Onfon Media API.

    The function first checks for environment variables. If they are not found,
    it falls back to using settings from the Django settings module.

    Args:
        recipients (list of str): List of phone numbers to send the message to.
        message (str): The message to be sent.

    Returns:
        list of dict: A list of responses from the API for each batch of messages sent.
                      Each response contains the API's response or an error message.

    Raises:
        ValueError: If the required configuration settings are missing.
    """
    api_url = os.getenv('SMS_API_URL', getattr(settings, 'SMS_API_URL', None))
    client_id = os.getenv('SMS_CLIENT_ID', getattr(
        settings, 'SMS_CLIENT_ID', None))
    api_key = os.getenv('SMS_API_KEY', getattr(settings, 'SMS_API_KEY', None))
    sender_id = os.getenv('SMS_SENDER_ID', getattr(
        settings, 'SMS_SENDER_ID', None))

    missing_settings = []
    if not api_url:
        missing_settings.append('SMS_API_URL')
    if not client_id:
        missing_settings.append('SMS_CLIENT_ID')
    if not api_key:
        missing_settings.append('SMS_API_KEY')
    if not sender_id:
        missing_settings.append('SMS_SENDER_ID')

    if missing_settings:
        raise ValueError(f"Missing required SMS configuration settings: {\
                         ', '.join(missing_settings)}")

    max_numbers_per_packet = 20
    max_requests_per_second = 40

    headers = {'Content-Type': 'application/json'}

    def send_request(batch):
        """
        Sends a batch of SMS messages to the API.

        Args:
            batch (list of str): List of phone numbers in the current batch.

        Returns:
            dict: The API's response or an error message.
        """
        data = {
            "SenderId": sender_id,
            "MessageParameters": [
                {"Number": number, "Text": message} for number in batch
            ],
            "ApiKey": api_key,
            "ClientId": client_id
        }

        data = json.dumps(data)

        try:
            response = requests.post(api_url, data=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    results = []
    for i in range(0, len(recipients), max_numbers_per_packet):
        batch = recipients[i:i + max_numbers_per_packet]
        result = send_request(batch)
        results.append(result)
        if (i // max_numbers_per_packet + 1) % max_requests_per_second == 0:
            time.sleep(1)  # Sleep for a second to maintain rate limit

    return results
