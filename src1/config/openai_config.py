# import os
# from dotenv import load_dotenv
# from src.config.openai_config import OpenAI

# load_dotenv()

# client = OpenAI(
#     api_key=os.getenv("OPENAI_API_KEY")
# )
from transformers import pipeline

# load model
generator = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

def generate_reminder(name, event):

    prompt = f"""
     Write a warm and friendly WhatsApp greeting message

    Person: {name}
    Event: {event}
    The message should:
    - start with Happy {event}
    - include positive wishes
    - sound natural and human
    - be 2–3 sentences long
    """

    result = generator(prompt, 
                       max_new_tokens=800,
                       do_sample=True,
                       temperature=1.35, 
                       top_p=0.85)

    return result[0]["generated_text"]

# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
# model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

# def generate_reminder(name, event):

#     prompt = f"""
#     Generate a short WhatsApp greeting message.

#     Person Name: {name}
#     Event Type: {event}

#     If event is birthday, say "Happy Birthday".
#     If event is anniversary, say "Happy Anniversary".
#     """

#     inputs = tokenizer(prompt, return_tensors="pt")
#     outputs = model.generate(**inputs, max_new_tokens=40)

#     return tokenizer.decode(outputs[0], skip_special_tokens=True)