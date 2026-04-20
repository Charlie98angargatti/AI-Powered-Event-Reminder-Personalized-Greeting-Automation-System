import requests
from config.whatsapp_config import WHATSAPP_URL, WHATSAPP_TOKEN

# def send_whatsapp_message(phone: str, message: str):
#     headers = {
#         "Authorization": f"Bearer {WHATSAPP_TOKEN}",
#         "Content-Type": "application/json"
#     }

#     data = {
#         "messaging_product": "whatsapp",
#         "to": phone,
#         "type": "text",
#         "text": {"body": message}
#     }

#     response = requests.post(WHATSAPP_URL, headers=headers, json=data)
#     return response.json()


def send_whatsapp_message(phone: str, message: str):  #just temproary

    print("Sending WhatsApp message")
    print("Phone:", phone)
    print("Message:", message)

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(WHATSAPP_URL, headers=headers, json=data)

    print("WhatsApp API Response:", response.json())

    return response.json()