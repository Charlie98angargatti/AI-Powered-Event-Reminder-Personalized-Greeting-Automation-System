from flask import Flask
from services.event_service1 import process_events

app = Flask(__name__)

@app.route("/run-reminder")

def run_reminder():

    process_events()

    return {"status": "Reminder executed"}

if __name__ == "__main__":
    app.run(port=5000)