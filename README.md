# Onfon-SMS-Sender
A Python package to send SMS using the Onfon Media API.


## Installation

```
pip install onfon-sms-sender

```

## Usage

```
from onfon_sms_sender import send_sms

recipients = ["254700000001", "254700000002"]
message = "Hello, this is a test message from Onfon Media API"
response = send_sms(recipients=recipients, message=message)
print(response)
```