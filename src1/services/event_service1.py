import json
from services.ai_service1 import generate_reminder
from services.whatsapp_service1 import send_whatsapp_message
from utils.date_utils import is_today_event

def process_events():

    with open("src/data/contacts.json") as f:
        contacts = json.load(f)

    for contact in contacts:

        if is_today_event(contact["date"]):

            message = generate_reminder(contact["name"], contact["event"])

            send_whatsapp_message(contact["phone"], message)