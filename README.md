
# Onfon-SMS-Sender
A Python package to send SMS using the Onfon Media API.


## Introduction
The Onfon-SMS-Sender package allows you to send SMS messages through the Onfon Media API. It supports configuration via environment variables, Django settings, or Flask settings, making it versatile and easy to integrate into various Python environments.

## Installation

```sh
pip install onfon-sms-sender
```

### Prerequisites
- Python 3.6 or higher
- Requests library
- Optional: Flask or Django for web application integration

## Configuration
The package requires the following configuration variables:

- `SMS_API_URL`
- `SMS_CLIENT_ID`
- `SMS_API_KEY`
- `SMS_SENDER_ID`

You can set these variables either as environment variables or in your application's settings.

## Usage

```python
from onfon_sms_sender import send_sms

recipients = []  # comma separated  List of string recipient phone numbers in format ["254...", "07.."]
message = "Hello, this is a test message from Onfon Media API"
response = send_sms(recipients=recipients, message=message)
print(response)
```

### Usage Example in Flask
You can set up your Flask application to use the `send_sms` function as shown below:

`app.py`
```python
from flask import Flask
from onfon_sms_sender import send_sms

app = Flask(__name__)
app.config['SMS_API_URL'] = 'https://api.onfonmedia.co.ke/v1/sms/SendBulkSMS'
app.config['SMS_CLIENT_ID'] = 'your_client_id_here'
app.config['SMS_API_KEY'] = 'your_api_key_here'
app.config['SMS_SENDER_ID'] = 'your_sender_id_here'

@app.route('/send_sms')
def send_sms_route():
    recipients = []# comma separated  List of string recipient phone numbers in format ["254...", "07.."]
    message = "Hello, this is a test message from Onfon Media API"
    response = send_sms(recipients=recipients, message=message)
    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
```

### Usage Example in Django
Ensure your Django project's `settings.py` includes the necessary configuration:

`settings.py`
```python
# settings.py
SMS_API_URL = 'https://api.onfonmedia.co.ke/v1/sms/SendBulkSMS'
SMS_CLIENT_ID = 'your_client_id_here'
SMS_API_KEY = 'your_api_key_here'
SMS_SENDER_ID = 'your_sender_id_here'
```

Use the `send_sms` function in your Django views:

```python
from django.http import JsonResponse
from onfon_sms_sender import send_sms

def send_sms_view(request):
    recipients = []  # comma separated  List of string recipient phone numbers in format ["254...", "07.."]
    message = "Hello, this is a test message from Onfon Media API"
    response = send_sms(recipients=recipients, message=message)
    return JsonResponse(response, safe=False)
```

## Running Tests
To run tests, ensure you have set the necessary environment variables or updated your `settings.py` file.

```sh
python -m unittest discover
```

## Feedback and Contribution
If you have any feedback or suggestions, please open an issue or submit a pull request on [GitHub](https://github.com/antonnifo/Onfon-SMS-Sender). Your contributions are welcome!

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
