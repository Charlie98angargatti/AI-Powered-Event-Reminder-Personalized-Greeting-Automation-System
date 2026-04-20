import json
import logging
from collections import defaultdict
from services.ai_service import generate_reminder, generate_combined_reminder
from services.email_service import send_email
from utils.date_utils import is_today_event
 
logging.basicConfig(level=logging.INFO)
LOG_FILE = "src/data/sent_log.json"
 
 
def load_log():
    try:
        with open(LOG_FILE) as f:
            return json.load(f)
    except Exception:
        return {}
 
 
def save_log(log):
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)
 
 
def process_events():
    """
    Load contacts, find today's events, group multiple events per person,
    generate AI greetings, and send emails.
    """
    try:
        with open("src/data/contact.json") as f:
            contacts = json.load(f)
    except Exception as e:
        logging.error(f"Failed to load contacts: {e}")
        return []
 
    # ── Step 1: Collect all contacts who have an event today ──────────────────
    # Group by (name, email) so if one person has birthday + anniversary today,
    # they get ONE combined email instead of two separate ones.
 
    grouped = defaultdict(lambda: {"email": "", "events": []})
 
    for contact in contacts:
        try:
            if is_today_event(contact["date"]):
                key = (contact["name"], contact["email"])
                grouped[key]["email"] = contact["email"]
                grouped[key]["events"].append(contact["event"])
                logging.info(
                    f"Event today → {contact['name']} | {contact['event']}"
                )
        except Exception as e:
            logging.error(f"Error reading contact {contact.get('name', '?')}: {e}")
 
    if not grouped:
        logging.info("No events found for today.")
        return []
 
    # ── Step 2: Generate messages and send emails ─────────────────────────────
    events_today = []
 
    for (name, email), data in grouped.items():
        try:
            events = data["events"]
 
            if len(events) == 1:
                # Single event → normal message
                message = generate_reminder(name, events[0])
                logging.info(f"Single event message generated for {name} ({events[0]})")
            else:
                # Multiple events on same day → combined message
                message = generate_combined_reminder(name, events)
                logging.info(
                    f"Combined message generated for {name} "
                    f"({', '.join(events)})"
                )
 
            print(f"\n{'='*60}")
            print(f"📧 To: {name} <{email}>")
            print(f"📅 Event(s): {', '.join(events)}")
            print(f"📝 Message:\n{message}")
            print(f"{'='*60}\n")
 
            send_email(email, message)
 
            events_today.append({
                "name": name,
                "email": email,
                "events": events
            })
 
        except Exception as e:
            logging.error(f"Error processing {name}: {e}")
 
    return events_today