import schedule
import time
from services.event_service import process_events
# from services.whatsapp_service import send_whatsapp_message
# from config.openai_config import generate_reminder
from services.ai_service import generate_reminder  # keep only one ai_service import


def run_job():
    events = process_events()
    for event in events:
        name = event["name"]
        phone = event["phone"]
        event_type = event["event"]
        message = generate_reminder(name, event_type)
        # send_whatsapp_message(phone, message)
    print("Job executed at:", time.strftime("%Y-%m-%d %H:%M:%S"))


# def start_scheduler():
#     # Schedule daily job at 20:10
#     schedule.every().day.at("20:27").do(run_job)

#     print("Scheduler started. Waiting for 20:27...")
    
#     while True:
#         schedule.run_pending()
#         time.sleep(10)  # check every 10 seconds


def start_scheduler():
    schedule.every().day.at("15:10").do(run_job)
    print("Scheduler started. Waiting for 18:24...")

    try:
        while True:
            schedule.run_pending()
            time.sleep(10)
    except KeyboardInterrupt:
        print("Scheduler stopped manually.")
    except Exception as e:
        print("Scheduler crashed:", e)











# import schedule
# import time
# from services.event_service import process_events
# from services.whatsapp_service import send_whatsapp_message
# from config.openai_config import generate_reminder
# from services.ai_service import generate_reminder


# def run_job():

#     events = process_events()

#     for event in events:

#         name = event["name"]
#         phone = event["phone"]
#         event_type = event["event"]

#         message = generate_reminder(name, event_type)

#         send_whatsapp_message(phone, message)


# def start_scheduler():

#     schedule.every().day.at("20:10").do(run_job)
#     # run_job()
#     while True:
#         schedule.run_pending()
#         time.sleep(60)

# # import schedule
# # import time
# # from src.services.event_service import process_events

# # def start_scheduler():
# #     # run every day at 9 AM
# #     schedule.every().day.at("09:00").do(process_events)

# #     while True:
# #         schedule.run_pending()
# #         time.sleep(60)

