import json
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("chatbot.log")
    ]
)
logger = logging.getLogger(__name__)

class CLIChatbot:

    def __init__(self):
        self.conversation = []
        self.model = "claude-sonnet-4-6"
        self.filename = "chat_history.json"
        logger.info("CLIChatbot initialized")

    def load(self):
        try:
            with open(self.filename, "r") as file:
                content = file.read()
                if content:
                    self.conversation = json.loads(content)
                    logger.info(f"Loaded {len(self.conversation)} messages from disk")
                else:
                    logger.warning("History file empty — starting fresh")
        except FileNotFoundError:
            logger.warning("No history file found — starting fresh")
            self.conversation = []

    def add_message(self, role, content):
        if role not in ["user", "assistant"]:
            raise ValueError(f"Invalid role: {role}")
        if not content.strip():
            raise ValueError("Message cannot be empty")
        self.conversation.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        logger.debug(f"Message added — {role}: {len(content)} chars")

    def respond(self, user_input):
        self.add_message("user", user_input)
        bot_reply = f"Echo → {user_input}"
        self.add_message("assistant", bot_reply)
        return bot_reply

    def save(self):
        try:
            with open(self.filename, "w") as file:
                json.dump(self.conversation, file, indent=2)
            logger.info(f"Saved {len(self.conversation)} messages to {self.filename}")
        except Exception as e:
            logger.error(f"Failed to save: {e}")

    def show_history(self):
        if not self.conversation:
            print("No conversation history yet.")
            return
        print("\n── Conversation History ──")
        for message in self.conversation:
            role = message["role"].upper()
            content = message["content"]
            timestamp = message["timestamp"]
            print(f"{role} [{timestamp}]: {content}")
        print("──────────────────────────\n")

    def clear(self):
        self.conversation = []
        self.save()
        logger.info("Conversation cleared")
        print("Conversation cleared. Starting fresh!\n")

    def run(self):
        self.load()
        print("\n╔══════════════════════════════════════╗")
        print("║     🤖 CLI Chatbot — Module 01       ║")
        print("╚══════════════════════════════════════╝")
        print(f"Loaded {len(self.conversation)} messages from history")
        print("\nCommands: 'quit' · 'history' · 'clear'")
        print("────────────────────────────────────────\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() == "quit":
                    self.save()
                    print("\nConversation saved. Goodbye! 👋")
                    logger.info("Bot shut down by user")
                    break

                elif user_input.lower() == "history":
                    self.show_history()

                elif user_input.lower() == "clear":
                    self.clear()

                else:
                    reply = self.respond(user_input)
                    print(f"Bot: {reply}\n")

            except KeyboardInterrupt:
                self.save()
                print("\n\nInterrupted. Conversation saved. Goodbye! 👋")
                break

            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                print("Something went wrong. Try again.\n")

# --- start the bot ---
bot = CLIChatbot()
bot.run()