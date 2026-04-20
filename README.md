# AI Event Reminder
#Overview

This project is an AI-powered automated reminder system that detects important events such as birthdays and anniversaries and sends personalized greeting messages automatically via email.
The system uses a language model to generate dynamic, human-like messages instead of static templates, improving personalization and user experience.

##Problem Statement
People often:

Forget important events like birthdays and anniversaries
Send generic or repetitive messages
Manually manage reminders and notifications

Solution

This project automates the entire process by:

Detecting events from stored data
Generating personalized greetings using AI
Sending emails automatically without manual intervention ,  [actaully i am planning to implement to whatsapp it's inprogress] 

#Key Features

Event detection based on date
AI-generated personalized messages
Automated email delivery using SMTP
REST API integration using Flask
Lightweight and scalable design
Supports multiple events on the same day

#System Architecture

contact.json
      ↓
Event Detection (event_service.py)
      ↓
AI Message Generation (ai_service.py)
      ↓
Email Service (email_service.py)
      ↓
Recipient receives email

#Technologies Used

Python
Flask (REST API)
Hugging Face Transformers (SmolLM2 Model)
SMTP (Email Automation)
JSON (Data Storage)


#Project Structure

src/
│
├── api.py                 # Flask API entry point
├── main.py               # Scheduler trigger
│

├── config/
│   └── openai_config.py / whatsapp_config.py
│

├── data/
│   ├── contact.json      # Event data
│   └── sent_log.json     # Logs
│

├── services/
│   ├── ai_service.py     # AI message generation
│   ├── email_service.py  # Email sending logic
│   └── event_service.py  # Event processing
│

├── utils/
│   └── date_utils.py     # Date matching logic
│

└── scheduler/
    └── job_scheduler.py  # Automation scheduler


#Workflow
Load contact data from JSON
Check if today's date matches any event
Generate a personalized message using AI
Send the message via email
Repeat daily via scheduler or API trigger
