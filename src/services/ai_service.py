
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "HuggingFaceTB/SmolLM2-360M-Instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)


def generate_reminder(name, event):

    sender = "Muruli"

    prompt = f"Write one short positive sentence for a {event} greeting."

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_new_tokens=25,
        temperature=0.5,
        top_p=0.9,
        repetition_penalty=1.2,
        no_repeat_ngram_size=3,
        do_sample=True
    )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # remove the prompt part
    wish = generated_text.replace(prompt, "").strip()

    # safety fallback (in case the model outputs nonsense)
    if len(wish) < 10:
        if event.lower() == "birthday":
            wish = "Wishing you a wonderful day filled with happiness and success."
        elif event.lower() == "anniversary":
            wish = "Wishing you both a beautiful life together filled with love and joy."
        else:
            wish = "Wishing you a wonderful day filled with happiness."

    message = f"""Happy {event.capitalize()} {name}! 🎉

{wish}

Best wishes,
{sender}
"""

    return message




# ============================================================
# APPROACH 2: Local Hugging Face — Proper Instruction Model
# ============================================================
# Problem with your old model (SmolLM2-360M):
#   → Only 360M params — too small to follow instructions
#   → Can't reliably write "exactly 2 sentences"
#   → That's why your fallback always triggered
#
# This uses Qwen2.5-1.5B-Instruct — still lightweight but
# actually follows instructions properly.
#
# Setup:
#   pip install transformers torch accelerate
#
# RAM requirements:
#   Qwen2.5-1.5B  → ~3GB RAM  (recommended, fast)
#   Qwen2.5-3B    → ~6GB RAM  (better quality)
#   Phi-3-mini    → ~8GB RAM  (Microsoft, very good)
# ============================================================
 
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# import torch
 
# # ✅ Choose your model based on your RAM:
# MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"   # ~3GB RAM — recommended
# # MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"   # ~6GB RAM — better quality
# # MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"  # ~8GB RAM — excellent
 
# print(f"[AI] Loading model: {MODEL_NAME} ...")
 
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForCausalLM.from_pretrained(
#     MODEL_NAME,
#     dtype=torch.float32,  # use float16 if you have a GPU
# )              

# # Use the pipeline with chat template — this is the correct way
# # to talk to instruction-tuned models
# generator = pipeline(
#     "text-generation",
#     model=model,
#     tokenizer=tokenizer,
# )
 
# print("[AI] Model loaded successfully ✅")
 
 
# def generate_reminder(name, event):
 
#     sender = "Muruli"
 
#     # Instruction-tuned models need messages in chat format
#     messages = [
#         {
#             "role": "system",
#             "content": (
#                 "You are a warm and friendly greeting message writer. "
#                 "Write short, heartfelt, personalized greetings. "
#                 "Follow instructions exactly. Output only what is asked."
#             )
#         },
#         {
#             "role": "user",
#             "content": (
#                 f"Write a personalized {event} greeting for {name}.\n"
#                 f"Rules:\n"
#                 f"- Exactly 2 sentences\n"
#                 f"- Mention {name} by name naturally\n"
#                 f"- Warm and sincere tone\n"
#                 f"- No hashtags, no emojis, no sign-off\n"
#                 f"- Output only the 2 sentences, nothing else"
#             )
#         }
#     ]
 
#     try:
#         # Apply the model's built-in chat template
#         text = tokenizer.apply_chat_template(
#             messages,
#             tokenize=False,
#             add_generation_prompt=True
#         )
 
#         output = generator(
#             text,
#             max_new_tokens=100,
#             temperature=0.7,
#             top_p=0.9,
#             repetition_penalty=1.1,
#             do_sample=True,
#             return_full_text=False,   # ← KEY: returns only new tokens, not prompt
#         )
 
#         wish = output[0]["generated_text"].strip()
 
#         # Light cleanup: take only first 2 sentences if model over-generates
#         import re
#         sentences = re.split(r'(?<=[.!?])\s+', wish)
#         wish = " ".join(sentences[:2]).strip()
 
#     except Exception as e:
#         print(f"[HuggingFace Error] {e}")
#         wish = (
#             f"Wishing you a truly special {event}, {name}!\n"
#             "May this day bring you endless joy and beautiful memories."
#         )
 
#     message = f"""Happy {event.capitalize()} {name}! 🎉
 
# {wish}
 
# Best wishes,
# {sender}
# """
 
#     return message

# src/services/ai_service.py
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# import torch
# import re

# MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

# # Globals for lazy loading
# tokenizer = None
# model = None
# generator = None

# def load_model():
#     global tokenizer, model, generator
#     if tokenizer is None or model is None or generator is None:
#         print(f"[AI] Loading model: {MODEL_NAME} ...")
#         # Load tokenizer and model
#         tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
#         model = AutoModelForCausalLM.from_pretrained(
#             MODEL_NAME,
#             dtype=torch.float32,  # CPU only
#         )
#         generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
#         print("[AI] Model loaded successfully ✅")

# def generate_reminder(name, event):
#     load_model()  # ensure model is loaded

#     # Simple prompt (avoid apply_chat_template which is not standard)
#     prompt = (
#         f"Write a warm, heartfelt {event} greeting for {name}. "
#         "Exactly 2 sentences, mention the name naturally, warm tone."
#     )

#     try:
#         output = generator(
#             prompt,
#             max_new_tokens=100,
#             temperature=0.7,
#             top_p=0.9,
#             repetition_penalty=1.1,
#             do_sample=True,
#             return_full_text=False
#         )
#         wish = output[0]["generated_text"].strip()
#         # Only take first 2 sentences
#         sentences = re.split(r'(?<=[.!?])\s+', wish)
#         wish = " ".join(sentences[:2]).strip()
#     except Exception as e:
#         print(f"[HuggingFace Error] {e}")
#         wish = f"Wishing you a truly special {event}, {name}!\nMay this day bring you joy and beautiful memories."

#     message = f"""Happy {event.capitalize()} {name}! 🎉

# {wish}

# Best wishes,
# Muruli
# """
#     return message









# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch

# # Load SmolLM2 model
# MODEL_NAME = "HuggingFaceTB/SmolLM2-360M-Instruct"

# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# def generate_reminder(name, event):

#     sender = "Muruli"

#     # Prompt for the model
#     prompt = f"""
# Write two short friendly sentences wishing someone a happy {event}.
# Do not include names.
# Keep it positive and natural.
# """

#     inputs = tokenizer(prompt, return_tensors="pt")

#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=60,
#         min_new_tokens=30,
#         temperature=0.7,
#         top_p=0.9,
#         repetition_penalty=1.2,
#         do_sample=True
#     )

#     generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     # Remove the prompt text from output
#     wishes = generated_text.replace(prompt, "").strip()

#     # Final structured message
#     message = f"""Happy {event.capitalize()} {name}! 🎉

# {wishes}

# Best wishes,
# {sender}
# """

#     return message


# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
# model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

# def generate_reminder(name, event):

#     sender = "Muruli"

#     prompt = f"""
# Write ONE short sentence wishing someone a happy {event}.
# Keep it positive and simple.
# Do not mention other holidays.
# """

#     inputs = tokenizer(prompt, return_tensors="pt")

#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=30,
#         min_new_tokens=10,
#         temperature=0.7,
#         repetition_penalty=1.4,
#         no_repeat_ngram_size=2
#     )

#     wish = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     message = f"""Happy {event.capitalize()} {name}! 🎉

# {wish}

# Best wishes,
# {sender}
# """

#     return message

# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
# model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")


# def generate_reminder(name, event):

#     sender = "Muruli"

#     prompt = f"""
# Complete the greeting message below.

# Happy {event} {name}! 🎉

# Wishing you a wonderful day filled with happiness and joy.
# May the coming year bring you success, good health, and beautiful memories.

# Best wishes,
# {sender}
# """

#     inputs = tokenizer(prompt, return_tensors="pt")

#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=120,
#         min_new_tokens=80,   # forces multi-line output
#         do_sample=True,
#         temperature=0.7,
#         top_p=0.9
#     )

#     message = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     return message



# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
# model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

# def generate_reminder(name, event):

#     sender = "Muruli"  # the person sending the greeting

#     prompt = f"""
# You are writing a greeting message.

# Sender: {sender}
# Receiver: {name}

# Event: {event}

# Write a warm and friendly greeting message.

# Rules:
# - Start with "Happy {event} {name}!"
# - Write exactly 2-3 sentences
# - Do NOT say that {name} is wishing someone.
# - Sound natural and cheerful
# - End the message with "Best wishes, {sender}"
# """

#     inputs = tokenizer(prompt, return_tensors="pt")

#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=100,
#         do_sample=True,
#         temperature=0.8,
#         top_p=0.9
#     )

#     message = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     return message






# def generate_reminder(name, event, sender):
#     # Event-specific prompt text
#     if event.lower() == "birthday":
#         event_prompt = "Wishing you happiness and success in the coming year. Enjoy your special day to the fullest!"
#     elif event.lower() == "anniversary":
#         event_prompt = "May your love grow stronger with each passing day. Enjoy your journey together!"
#     else:
#         event_prompt = "May this special day bring you joy, happiness, and all the best things in life."

#     # Construct the prompt for the model
#     prompt = f"""
#     Generate a birthday greeting message.

#     Receiver Name: {name}
#     Event: {event}
#     Sender: {sender}

#     Instructions:
#     - Start with "Happy {event} {name}!"
#     - Write 2-3 warm, personalized sentences about the event.
#     - Include good wishes for the future.
#     - End with "Best wishes, {sender}".

#     Example format:
#     Happy {event} {name}!
#     Wishing you happiness and success in the coming year.
#     Enjoy your special day to the fullest!

#     Best wishes,
#     {sender}
#     """

#     # Tokenize the prompt and generate the response
#     inputs = tokenizer(prompt, return_tensors="pt")
    
#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=120,
#         min_length=40,
#         do_sample=True,
#         temperature=0.8,
#         top_p=0.9
#     )

#     # Decode the output
#     message = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     # Process the message and format it with newlines
#     sentences = message.split('. ')
#     message_with_newlines = '\n'.join([sentence.strip() + '.' for sentence in sentences if sentence])

#     return message_with_newlines
# def generate_reminder(name, event):
#     sender = "Muruli"

#     if event.lower() == "birthday":
#         event_prompt = "Wish them happiness, success, and a wonderful year ahead."
#     elif event.lower() == "anniversary":
#         event_prompt = "Wish them love, togetherness, and a beautiful journey ahead."
#     else:
#         event_prompt = "Write a warm congratulatory message."

#     prompt = f"""
# Generate a warm greeting message for a {event}. The message should include:
# - A start like "Happy {event} {name}!"
# - At least two warm, personalized sentences wishing {name} well for their {event}.
# - Use the event's context to add a specific message (e.g., happiness for a birthday, love for an anniversary).
# - End with "Best wishes, {sender}".

# Example:
# "Happy birthday Karthik!
# Wishing you happiness and success in the coming year.
# Enjoy your special day to the fullest!

# Best wishes,
# {sender}"
# """

#     inputs = tokenizer(prompt, return_tensors="pt")

#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=120,
#         min_length=40,
#         do_sample=True,
#         temperature=0.8,
#         top_p=0.9
#     )

#     # Decode the generated tokens into a human-readable string
#     message = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     # Split the message by periods and add newlines for each sentence
#     sentences = message.split('. ')
#     message_with_newlines = '\n'.join([sentence.strip() + '.' for sentence in sentences if sentence])

#     return message_with_newlines
# def generate_reminder(name, event):

#     sender = "Muruli"

#     if event.lower() == "birthday":
#         event_prompt = "Wish them happiness, success, and a wonderful year ahead."

#     elif event.lower() == "anniversary":
#         event_prompt = "Wish them love, togetherness, and a beautiful journey ahead."

#     else:
#         event_prompt = "Write a warm congratulatory message."

#     prompt = f"""
# Generate a greeting message.

# Receiver Name: {name}
# Event: {event}
# Sender: {sender}

# Instructions:
# - Start with "Happy {event} {name}!"
# - Write 2–3 warm sentences.
# - {event_prompt}
# - End with "Best wishes, {sender}"

# Format example:
# Happy {event} {name}!
# <2 sentences of wishes>

# Best wishes,
# {sender}
# """

#     inputs = tokenizer(prompt, return_tensors="pt")

#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=120,
#         min_length=40,
#         do_sample=True,
#         temperature=0.8,
#         top_p=0.9
#     )

#     message = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     return message


# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
# model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
# model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

# def generate_reminder(name, event):

#     prompt = f"""
#     Write a warm and friendly greeting message.

#     Person: {name}
#     Event: {event}

#     Requirements:
#     - Start with Happy {event} {name}
#     - Write 2–3 sentences
#     - Include positive wishes
#     """

#     inputs = tokenizer(prompt, return_tensors="pt")

#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=80,
#         do_sample=True,
#         temperature=0.9,
#         top_p=0.9
#     )

#     return tokenizer.decode(outputs[0], skip_special_tokens=True)

# from transformers import pipeline

# generator = pipeline(
#     "text2text-generation",
#     model="google/flan-t5-base"
# )

# def generate_reminder(name, event):

#     prompt = f"""
#     Write a warm and friendly greeting message.

#     Person: {name}
#     Event: {event}

#     Requirements:
#     - Start with "Happy {event} {name}"
#     - Write 2 to 3 sentences
#     - Include positive wishes
#     - Sound natural and human
#     """
#     inputs= tokenizer(promt,return_tensors='pt')

#     result = model.generate(
#         **inputs,
#         max_new_tokens=80,
#         do_sample=True,
#         temperature=0.9,
#         top_p=0.9
#     )
#     message = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return message



# from transformers import pipeline

# generator = pipeline(
#     "text2text-generation",
#     model="google/flan-t5-base"
# )

# def generate_reminder(name, event):

#     prompt = f"""
#     Write a short friendly WhatsApp greeting.

#     Person: {name}
#     Event: {event}
#     """

#     result = generator(prompt, max_length=60)

#     return result[0]["generated_text"]


# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# model_name = "google/flan-t5-base"

# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# generator = pipeline(
#     "text-generation",
#     model=model,
#     tokenizer=tokenizer
# )

# def generate_reminder(name, event):

#     prompt = f"Write a short WhatsApp message wishing {name} a happy {event}"

#     result = generator(prompt, max_length=50)

#     return result[0]["generated_text"]

# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
# model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

# def generate_reminder(name, event):
#     prompt = f"Write a short WhatsApp message wishing {name} a happy {event}"
#     inputs = tokenizer(prompt, return_tensors="pt")
#     outputs = model.generate(**inputs, max_new_tokens=50)
#     return tokenizer.decode(outputs[0], skip_special_tokens=True)   
