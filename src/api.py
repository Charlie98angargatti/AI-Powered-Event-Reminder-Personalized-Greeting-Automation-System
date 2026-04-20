# from flask import Flask, jsonify
# from services.event_service import process_events

# app = Flask(__name__)

# @app.route("/run-reminder", methods=["GET"])
# def run_reminder():

#     process_events()

#     return jsonify({
#         "status": "success",
#         "message": "Reminder workflow executed"
#     })


# if __name__ == "__main__":
#     app.run(port=5000)   


# from flask import Flask, jsonify
# from services.event_service import process_events

# app = Flask(__name__)


# @app.route("/run-reminder", methods=["GET"])
# def run_reminder():
#     events_today = process_events()

#     if events_today:
#         return jsonify({
#             "status": "success",
#             "message": f"Reminders sent for {len(events_today)} contact(s).",
#             "events_processed": [
#                 {
#                     "name": e["name"],
#                     "events": e["events"]
#                 }
#                 for e in events_today
#             ]
#         })
#     else:
#         return jsonify({
#             "status": "success",
#             "message": "No events found for today. No emails sent."
#         })


# if __name__ == "__main__":
#     app.run(port=5000, debug=False)  



from flask import Flask, jsonify
from services.event_service import process_events

app = Flask(__name__)

@app.route("/run-reminder", methods=["GET"])
def run_reminder():
    events_today = process_events()

    if events_today:
        return jsonify({
            "status": "success",
            "message": f"Reminders sent for {len(events_today)} contact(s).",
            "events_processed": [
                {
                    "name": e["name"],
                    "events": [e["event"]]  # Wrap single event in a list
                }
                for e in events_today
            ]
        })
    else:
        return jsonify({
            "status": "success",
            "message": "No events found for today. No emails sent."
        })

if __name__ == "__main__":
    app.run(port=5000, debug=False)