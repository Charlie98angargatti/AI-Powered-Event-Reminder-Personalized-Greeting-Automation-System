import requests
from config.whatsapp_config import WHATSAPP_URL, WHATSAPP_TOKEN

def send_whatsapp_message(phone, message):

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

    return response.json()