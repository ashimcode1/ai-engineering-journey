import json
from datetime import datetime
class ConversationBot:
    def __init__(self):
        self.conversation=[]
        self.model="claude-sonnet-4-6"
        self.filename="history.json"
    
    def load(self):
        try:
            with open(self.filename,'r') as file:
                content=file.read()
            if content:
                self.conversation = json.loads(content)  
        except FileNotFoundError:
            self.conversation = []
    
    def add(self,role,content):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversation.append({
            "role":role,
            "content":content,
            "timestamp":timestamp})
    
    def show(self):
        for message in self.conversation:
            print(f"{message['role'].upper()}: {message['content']} |{message['timestamp']}")

    
    def save(self):
        with open(self.filename,'w') as file:
            json.dump(self.conversation,file,indent=2)
        print(f"Saved {len(self.conversation)} messages to {self.filename}")

    def summary(self):
        total_chars = sum(len(m["content"]) for m in self.conversation)
        print(f"Model       : {self.model}")
        print(f"Messages    : {len(self.conversation)}")
        print(f"Total chars : {total_chars}")
    
bot = ConversationBot()
bot.load()
bot.add("user", "What is AI?")
bot.add("assistant", "AI is artificial intelligence.")
bot.show()
bot.save()
bot.summary()