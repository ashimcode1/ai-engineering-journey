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
        pass

    def add_message(self, role, content):
        pass

    def respond(self, user_input):
        pass

    def save(self):
        pass

    def show_history(self):
        pass

    def clear(self):
        pass

    def run(self):
        pass

bot = CLIChatbot()
bot.run()