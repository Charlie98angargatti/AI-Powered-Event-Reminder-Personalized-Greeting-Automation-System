from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
import re
 
# ✅ Recommended: ~3GB RAM — follows instructions well
MODEL_NAME =  "Qwen/Qwen2.5-0.5B-Instruct"
 
# Uncomment for tighter RAM (~1GB) — less reliable instruction-following:
# MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
 
# Uncomment for best quality (~8GB RAM):
# MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"
 
print(f"[AI] Loading model: {MODEL_NAME} ...")
 
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32,  # use torch.float16 if you have a GPU
)
 
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)
 
print("[AI] Model loaded successfully ✅")
 
 
def clean_generated_text(text: str) -> str:
    """
    Extract exactly 2 clean sentences from the model output.
    Removes unwanted preamble, labels, or extra lines.
    """
    text = text.strip()
 
    # Remove common preamble patterns like "Here is...", "Sure!", "Message:", etc.
    text = re.sub(
        r'^(sure[!,.]?|here\s+(is|are)[^:]*:|message:|greeting:|output:|of course[!,.]?)\s*',
        '', text, flags=re.IGNORECASE
    ).strip()
 
    # Split into sentences using punctuation boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text)
 
    # Filter out very short fragments (less than 5 words)
    sentences = [s.strip() for s in sentences if len(s.split()) >= 5]
 
    if len(sentences) >= 2:
        return " ".join(sentences[:2])
    elif len(sentences) == 1:
        return sentences[0]
    else:
        return text  # fallback: return cleaned raw text
 
 
def generate_greeting(name: str, event: str) -> str:
    """
    Generate a 2-sentence personalized greeting for the given name and event.
    Event examples: 'birthday', 'anniversary'
    """
    event_lower = event.strip().lower()
 
    # Tailor the prompt based on event type
    if event_lower == "birthday":
        context = "birthday celebration"
        tone_hint = "joyful, warm, and celebratory"
    elif event_lower == "anniversary":
        context = "wedding anniversary milestone"
        tone_hint = "loving, heartfelt, and meaningful"
    else:
        context = event_lower
        tone_hint = "warm and sincere"
 
    messages = [
        {
            "role": "system",
            "content": (
                "You are a greeting card writer. "
                "You write short, heartfelt, personalized messages. "
                "You ALWAYS follow the format instructions exactly. "
                "You output ONLY the greeting — no extra text, no labels, no sign-off."
            )
        },
        {
            "role": "user",
            "content": (
                f"Write a {context} greeting for {name}.\n\n"
                f"Requirements:\n"
                f"- Write EXACTLY 2 sentences.\n"
                f"- Sentence 1: A warm {tone_hint} wish that mentions {name} by name.\n"
                f"- Sentence 2: A sincere, uplifting thought related to {context}.\n"
                f"- No hashtags, no emojis, no sign-off, no labels.\n"
                f"- Output ONLY the 2 sentences, nothing else.\n\n"
                f"Example format (do not copy this content, just the structure):\n"
                f"Wishing you a wonderful day, [Name], filled with everything you love. "
                f"May this special occasion bring you joy that lasts all year long."
            )
        }
    ]
 
    try:
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
 
        output = generator(
            text,
            max_new_tokens=120,
            temperature=0.75,
            top_p=0.9,
            repetition_penalty=1.15,
            do_sample=True,
            return_full_text=False,
        )
 
        raw = output[0]["generated_text"]
        wish = clean_generated_text(raw)
 
    except Exception as e:
        print(f"[AI Error] {e}")
        # Fallback messages by event type
        fallbacks = {
            "birthday": (
                f"Wishing you a truly wonderful birthday, {name}, surrounded by everyone you love. "
                f"May this special day mark the beginning of your best year yet."
            ),
            "anniversary": (
                f"Happy Anniversary, {name} — may your bond continue to grow stronger with every passing year. "
                f"Here's to celebrating the beautiful journey you've built together."
            ),
        }
        wish = fallbacks.get(event_lower, (
            f"Wishing you a very special {event}, {name}! "
            f"May this day bring you endless joy and beautiful memories."
        ))
 
    return wish
 
 
def generate_reminder(name: str, event: str) -> str:
    """
    Build the full email message for a single person and event.
    """
    sender = "Muruli"
    event_display = event.strip().capitalize()
    wish = generate_greeting(name, event)
 
    message = (
        f"Happy {event_display}, {name}! 🎉\n\n"
        f"{wish}\n\n"
        f"Best wishes,\n"
        f"{sender}"
    )
    return message
 
 
def generate_combined_reminder(name: str, events: list) -> str:
    """
    Build a combined email message when a person has multiple events on the same day.
    Each event gets its own personalized 2-sentence greeting.
 
    Args:
        name: Person's name
        events: List of event strings e.g. ['birthday', 'anniversary']
    """
    sender = "Muruli"
    sections = []
 
    for event in events:
        event_display = event.strip().capitalize()
        wish = generate_greeting(name, event)
        section = f"🎉 Happy {event_display}, {name}!\n{wish}"
        sections.append(section)
 
    combined_wishes = "\n\n".join(sections)
 
    message = (
        f"Dear {name},\n\n"
        f"Today is a very special day for you — you have multiple celebrations!\n\n"
        f"{combined_wishes}\n\n"
        f"Best wishes,\n"
        f"{sender}"
    )
    return message