import json
import requests
from django.conf import settings
import time


def send_sms(recipients, message):
    api_url = settings.SMS_API_URL
    client_id = settings.SMS_CLIENT_ID
    api_key = settings.SMS_API_KEY
    sender_id = settings.SMS_SENDER_ID
    max_numbers_per_packet = 20
    max_requests_per_second = 40

    headers = {'Content-Type': 'application/json'}

    def send_request(batch):
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
