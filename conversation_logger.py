import json
from datetime import datetime

def load_conversation(filename="history.json"):
    try:
        with open(filename, "r") as file:
            content = file.read()
            if not content:              # ← if file is empty
                return []
            return json.loads(content)   # ← parse the string
    except FileNotFoundError:
        return []

def add_message(conversation, role, content):
    conversation.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return conversation

def print_conversation(conversation):
    for message in conversation:
        print(f"{message['role'].upper()}: {message['content']} | Time:{message['timestamp']}")

def save_conversation(conversation, filename="history.json"):
    with open(filename, "w") as file:
        json.dump(conversation, file, indent=2)
    print(f"Saved {len(conversation)} messages to {filename}")

# --- main program ---
conversation = load_conversation()
print(f"Loaded {len(conversation)} messages from disk")

add_message(conversation, "user", "What is AI?")
add_message(conversation, "assistant", "AI is artificial intelligence.")
add_message(conversation, "user", "Hi!")

print_conversation(conversation)
save_conversation(conversation)