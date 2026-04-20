import json
import logging
from datetime import datetime
from services.ai_service import generate_reminder
from services.email_service import send_email
from utils.date_utils import is_today_event

logging.basicConfig(level=logging.INFO)
LOG_FILE = "src/data/sent_log.json"


def load_log():
    try:
        with open(LOG_FILE) as f:
            return json.load(f)
    except:
        return {}


def save_log(log):
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

def process_events():
    events_today = []
    try:
        # load contacts
        with open("src/data/contact.json") as f:
            contacts = json.load(f)

    except Exception as e:
        logging.error(f"Failed to load contacts: {e}")
        return

    for contact in contacts: #just temproriely

        try:
            if is_today_event(contact["date"]):

                logging.info(f"Event found for {contact['name']}")
                events_today.append(contact)

                # Generate AI reminder
                message = generate_reminder(contact["name"], contact["event"])

                print("AI Generated Message:", message)

                # Send via Email
                send_email(contact["email"], message)

        except Exception as e:
            logging.error(f"Error processing {contact['name']}: {e}")
    return events_today
    # for contact in contacts:     

    #     try:
    #         if is_today_event(contact["date"]):

    #             logging.info(f"Event found for {contact['name']}")
    #             events_today.append(contact)
    #             # generate AI reminder
    #             # message = generate_reminder(contact["name"], contact["event"])

    #             # send via WhatsApp
    #             # send_whatsapp_message(contact["phone"], message)

    #     except Exception as e:
    #         logging.error(f"Error processing {contact['name']}: {e}")
    # return events_today
# import json
# from src.services.ai_service import generate_reminder
# from src.services.whatsapp_service import send_whatsapp_message
# from src.utils.date_utils import is_today_event

# def process_events():
#     # load contacts
#     with open("src/data/contacts.json") as f:
#         contacts = json.load(f)

#     for contact in contacts:
#         if is_today_event(contact["date"]):
#             # generate AI reminder
#             message = generate_reminder(contact["name"], contact["event"])
#             # send via WhatsApp
#             send_whatsapp_message(contact["phone"], message)