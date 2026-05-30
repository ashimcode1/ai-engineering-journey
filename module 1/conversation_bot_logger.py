import json
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("bot.log")
    ]
)

logger = logging.getLogger(__name__)

class ConversationBot:

    def __init__(self):
        self.conversation = []
        self.model = "claude-sonnet-4-6"
        self.filename = "history.json"
        logger.info("ConversationBot initialized")

    def load(self):
        try:
            with open(self.filename, "r") as file:
                content = file.read()
                if content:
                    self.conversation = json.loads(content)
                    logger.info(f"Loaded {len(self.conversation)} messages from disk")
                else:
                    logger.warning("History file is empty — starting fresh")
        except FileNotFoundError:
            logger.warning(f"{self.filename} not found — starting fresh")
            self.conversation = []

    def add(self, role, content):
        if role not in ["user", "assistant"]:
            logger.error(f"Invalid role '{role}' — must be user or assistant")
            raise ValueError(f"Invalid role '{role}'")
        if not content.strip():
            logger.error("Empty message content rejected")
            raise ValueError("Message content cannot be empty")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation.append({
            "role": role,
            "content": content,
            "timestamp": timestamp
        })
        logger.debug(f"Message added — role: {role}, chars: {len(content)}")

    def show(self):
        for message in self.conversation:
            print(f"{message['role'].upper()}: {message['content']} | {message['timestamp']}")

    def save(self):
        try:
            with open(self.filename, "w") as file:
                json.dump(self.conversation, file, indent=2)
            logger.info(f"Saved {len(self.conversation)} messages to {self.filename}")
        except Exception as e:
            logger.error(f"Failed to save conversation: {e}")

    def summary(self):
        total_chars = sum(len(m["content"]) for m in self.conversation)
        logger.info(f"Summary — model: {self.model}, messages: {len(self.conversation)}, chars: {total_chars}")
        print(f"Model       : {self.model}")
        print(f"Messages    : {len(self.conversation)}")
        print(f"Total chars : {total_chars}")

# --- main program ---
bot = ConversationBot()
bot.load()
bot.add("user", "What is AI?")
bot.add("assistant", "AI is artificial intelligence.")
bot.show()
bot.save()
bot.summary()
bot.add("accountant", "hello")
bot.add("user", "   ")