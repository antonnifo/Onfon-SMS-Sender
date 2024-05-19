import json
import requests
import time
from dotenv import load_dotenv
import os

# Attempt to import Django settings
try:
    from django.conf import settings as django_settings
except ImportError:
    django_settings = None

# Attempt to import Flask app configuration
try:
    from flask import current_app as flask_app
except ImportError:
    flask_app = None

load_dotenv()  # Load environment variables from .env file


def get_config_value(key, default=None):
    """
    Get configuration value from environment variables, Django settings, or Flask settings.

    Args:
        key (str): The configuration key to look for.
        default: The default value to return if the key is not found.

    Returns:
        The configuration value.
    """
    if flask_app and key in flask_app.config:
        return flask_app.config[key]
    if django_settings and hasattr(django_settings, key):
        return getattr(django_settings, key)
    return os.getenv(key, default)


def send_sms(recipients, message):
    """
    Sends SMS messages to a list of recipients using the Onfon Media API.

    The function first checks for environment variables. If they are not found,
    it falls back to using settings from Flask or Django.

    Args:
        recipients (list of str): List of phone numbers to send the message to.
        message (str): The message to be sent.

    Returns:
        list of dict: A list of responses from the API for each batch of messages sent.
                      Each response contains the API's response or an error message.

    Raises:
        ValueError: If the required configuration settings are missing.
    """
    api_url = get_config_value(
        'SMS_API_URL', 'https://api.onfonmedia.co.ke/v1/sms/SendBulkSMS')
    client_id = get_config_value('SMS_CLIENT_ID', 'your_client_id_here')
    api_key = get_config_value('SMS_API_KEY', 'your_api_key_here')
    sender_id = get_config_value('SMS_SENDER_ID', 'Aqila-Alert')

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
