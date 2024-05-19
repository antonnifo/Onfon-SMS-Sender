# Onfon-SMS-Sender
A Python package to send SMS using the Onfon Media API.


## Installation

```
pip install onfon-sms-sender

```


## Configuration
The package requires the following configuration variables:

- SMS_API_URL
- SMS_CLIENT_ID
- SMS_API_KEY
- SMS_SENDER_ID

### Using Environment Variables
Create a .env file in your project root with the following content:
```
SMS_API_URL=https://api.onfonmedia.co.ke/v1/sms/SendBulkSMS
SMS_CLIENT_ID=your_client_id_here
SMS_API_KEY=your_api_key_here
SMS_SENDER_ID=Aqila-Alert
```


### Using Django Settings
Alternatively, you can set these variables in your Django settings.py file:

```
# settings.py
SMS_API_URL = 'https://api.onfonmedia.co.ke/v1/sms/SendBulkSMS'
SMS_CLIENT_ID = 'your_client_id_here'
SMS_API_KEY = 'your_api_key_here'
SMS_SENDER_ID = 'Your Sender ID'
```

## Usage

```
from onfon_sms_sender import send_sms

recipients = ["254700000001", "0700000002"] #put your phone numbers here using the format 254 or 07...
message = "Hello, this is a test message from Onfon Media API"
response = send_sms(recipients=recipients, message=message)
print(response)
```


## Running Tests
To run tests, ensure you have set the necessary environment variables or updated your `settings.py` file.

```
python -m unittest discover
```