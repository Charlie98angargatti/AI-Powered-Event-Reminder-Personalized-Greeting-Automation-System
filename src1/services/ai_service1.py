from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

def generate_reminder(name, event):

    prompt = f"Write a short WhatsApp message wishing {name} a happy {event}"

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(**inputs, max_new_tokens=40)

    message = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return message