# CLI Chatbot 🤖

A fully functional command-line chatbot built in Python — the Module 01 capstone project. Combines every concept from the module into one complete, production-quality application: OOP, persistent storage, logging, error handling, and a clean command interface.

> This is the foundation. In Module 03, the echo response gets replaced with a real Claude API call — turning this into a fully intelligent AI chatbot.

---

## What it does

- Loads previous conversation history on startup
- Accepts user input in a continuous loop
- Responds to messages (echo for now — Claude API coming in Module 03)
- Stores every message with timestamps in AI API format
- Saves conversation history to disk automatically
- Supports special commands: `history`, `clear`, `quit`
- Logs all activity to `chatbot.log`
- Handles errors gracefully — never crashes on the user

---

## How to run

```bash
# activate virtual environment
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

# run the chatbot
python cli_chatbot.py
```

**Example session:**
```
╔══════════════════════════════════════╗
║     🤖 CLI Chatbot — Module 01       ║
╚══════════════════════════════════════╝
Loaded 0 messages from history

Commands: 'quit' · 'history' · 'clear'
────────────────────────────────────────

You: Hello, I am learning AI engineering
Bot: Echo → Hello, I am learning AI engineering

You: history
── Conversation History ──
USER [2026-05-30 12:36:26]: Hello, I am learning AI engineering
ASSISTANT [2026-05-30 12:36:26]: Echo → Hello, I am learning AI engineering
──────────────────────────

You: clear
Conversation cleared. Starting fresh!

You: quit
Conversation saved. Goodbye! 👋
```

---

## Commands

| Command | What it does |
|---|---|
| Any text | Send a message and get a response |
| `history` | Display full conversation with timestamps |
| `clear` | Wipe conversation history from memory and disk |
| `quit` | Save conversation and exit |
| `Ctrl+C` | Force exit — still saves conversation |

---

## Class structure

Everything lives inside one class — `CLIChatbot`:

```python
bot = CLIChatbot()
bot.run()           # starts everything
```

### Methods

| Method | What it does |
|---|---|
| `__init__()` | Sets up conversation list, model name, filename |
| `load()` | Reads `chat_history.json` from disk on startup |
| `add_message(role, content)` | Validates and appends message with timestamp |
| `respond(user_input)` | Stores user message, generates and stores reply |
| `save()` | Writes conversation to `chat_history.json` |
| `show_history()` | Loops through and prints all messages |
| `clear()` | Resets conversation in memory and on disk |
| `run()` | Main loop — ties everything together |

---

## Conversation format

Every message is stored as a dict — the exact format AI APIs expect:

```json
[
  {
    "role": "user",
    "content": "Hello, I am learning AI engineering",
    "timestamp": "2026-05-30 12:36:26"
  },
  {
    "role": "assistant",
    "content": "Echo → Hello, I am learning AI engineering",
    "timestamp": "2026-05-30 12:36:26"
  }
]
```

When Claude API is plugged in during Module 03, this format requires zero changes.

---

## Logging

All activity is logged to `chatbot.log`:

```
2026-05-30 12:36:20 | INFO    | CLIChatbot initialized
2026-05-30 12:36:20 | WARNING | No history file found — starting fresh
2026-05-30 12:36:26 | DEBUG   | Message added — user: 35 chars
2026-05-30 12:36:26 | DEBUG   | Message added — assistant: 41 chars
2026-05-30 12:36:32 | INFO    | Saved 0 messages to chat_history.json
2026-05-30 12:36:33 | INFO    | Bot shut down by user
```

---

## Error handling

| Scenario | How it's handled |
|---|---|
| History file missing | Catches `FileNotFoundError`, starts fresh |
| Empty history file | Checks `if content` before parsing |
| Invalid role | Raises `ValueError` immediately |
| Empty message | Raises `ValueError` immediately |
| Save failure | Catches `Exception`, logs error, keeps running |
| `Ctrl+C` interrupt | Catches `KeyboardInterrupt`, saves before exiting |
| Any unexpected error | Caught in main loop, logged, bot keeps running |

---

## Concepts demonstrated

- Object-oriented programming — full class with 7 methods
- `while True` main loop with `break` and `continue`
- `input()` — reading user input from terminal
- Persistent state — conversation survives between sessions
- JSON storage — `json.dump()` and `json.loads()`
- Five-level logging — terminal + file output
- Defensive programming — validation before storage
- `KeyboardInterrupt` handling — graceful forced exit
- `.lower()` — case-insensitive command matching
- `.strip()` — cleaning user input

---

## What's next

In Module 03 this one line in `respond()`:

```python
bot_reply = f"Echo → {user_input}"
```

Gets replaced with:

```python
response = claude_client.messages.create(
    model="claude-sonnet-4-6",
    messages=self.conversation
)
bot_reply = response.content[0].text
```

Same class. Same methods. Same conversation format. Suddenly — a real AI chatbot.

---

## Requirements

Python 3.11+ · No external libraries needed.

---

## Author

Built as part of an AI Engineering learning journey — Module 01, Lesson 8 (Capstone).
