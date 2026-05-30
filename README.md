# API Tester 🌐

A Python project demonstrating how to make real HTTP API calls using the `requests` library — with proper error handling, logging, headers, and query parameters. Built as a foundation for calling AI APIs like Anthropic's Claude.

---

## What it does

- Fetches real live data from GitHub's public API
- Handles success, 404, timeout, and connection errors gracefully
- Uses headers and query parameters like a production API call
- Logs every step with timestamps and severity levels
- Returns clean Python dicts from JSON responses

---

## How to run

```bash
# activate your virtual environment first
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux

# install dependencies
pip install requests

# run
python api_tester.py
```

**Example output:**
```
2026-05-26 12:05:49 | INFO    | Fetching GitHub profile for: torvalds
2026-05-26 12:05:49 | INFO    | Success — got data for torvalds
Name        : Linus Torvalds
Username    : torvalds
Public repos: 11
Followers   : 304595
---
2026-05-26 12:05:50 | INFO    | Fetching top 5 repos for torvalds
2026-05-26 12:05:50 | INFO    | Got 5 repos
AudioNoise — ⭐ 4372
GuitarPedal — ⭐ 1939
1590A — ⭐ 566
libgit2 — ⭐ 358
HunspellColorize — ⭐ 344
---
2026-05-26 12:05:51 | WARNING | User 'thisuserdoesnotexist99999' not found on GitHub
User not found — returned None as expected
```

---

## How it works

### Fetching a user profile

```python
user = fetch_github_user("torvalds")
if user:
    print(f"Name     : {user['name']}")
    print(f"Followers: {user['followers']}")
```

### Fetching top repos by stars

```python
repos = fetch_github_repos("torvalds", max_repos=5)
for repo in repos:
    print(f"{repo['name']} — ⭐ {repo['stargazers_count']}")
```

---

## Key concepts

### Status codes — what the server says back

| Code | Meaning | How we handle it |
|---|---|---|
| `200` | Success | Parse JSON and return data |
| `404` | Not found | Log WARNING, return None |
| `429` | Rate limited | Log ERROR, return None |
| `500` | Server error | Log ERROR, return None |

### Headers — metadata sent with the request

```python
headers = {
    "Accept": "application/vnd.github.v3+json"
}
```

Headers carry extra information alongside your request. When calling AI APIs, your API key goes here — never in the URL.

### Query parameters — filters and options

```python
params = {
    "sort": "stars",
    "direction": "desc",
    "per_page": 5
}
```

`requests` automatically converts this dict into a URL query string:
```
/repos?sort=stars&direction=desc&per_page=5
```

### Timeout — protection against hanging forever

```python
requests.get(url, timeout=10)
```

Without a timeout, your program waits forever if the server is down. Always set one.

---

## Error handling

Every possible failure is caught and logged:

```python
except requests.exceptions.Timeout:
    logger.error("Request timed out — server took too long")
    return None

except requests.exceptions.ConnectionError:
    logger.error("No internet connection")
    return None
```

---

## Concepts demonstrated

- HTTP GET requests with `requests` library
- Status code handling — 200, 404, and unexpected codes
- Headers and query parameters
- `timeout` protection
- Five-level logging — DEBUG through ERROR
- Defensive programming — always return something, never crash silently
- JSON response parsing with `response.json()`

---

## Why this matters for AI engineering

This is the exact same pattern used to call AI APIs:

```python
# GitHub API (this project)
response = requests.get(
    "https://api.github.com/users/torvalds",
    headers={"Accept": "application/vnd.github.v3+json"},
    timeout=10
)

# Claude API (coming in Module 3)
response = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={"x-api-key": "your-key", "anthropic-version": "2023-06-01"},
    json={"model": "claude-sonnet-4-6", "messages": [...]},
    timeout=30
)
```

Same structure. Different URL, different headers, different data. Master this pattern here and calling Claude's API will feel natural.

---

## Requirements

```
requests==2.33.1
```

Install with:
```bash
pip install -r requirements.txt
```

---

## Author

Built as part of an AI Engineering learning journey — Module 01, Lesson 6.
